import itertools
import json
import re

from bs4 import BeautifulSoup

from zdict.dictionary import DictBase
from zdict.exceptions import NotFoundError
from zdict.models import Record


class YahooDict(DictBase):

    API = 'https://tw.dictionary.search.yahoo.com/search?p={word}'

    @property
    def provider(self):
        return 'yahoo'

    @property
    def title(self):
        return 'Yahoo Dictionary'

    def _get_url(self, word) -> str:
        return self.API.format(word=word)

    def show(self, record: Record):
        content = json.loads(record.content)

        # print word
        self.color.print(content['word'], 'yellow')

        # print pronounce
        for k, v in content.get('pronounce', []):
            self.color.print(k, end='')
            self.color.print(v, 'lwhite', end=' ')
        print()

        # print explain
        main_explanations = content.get('explain', [])
        if self.args.verbose:
            main_explanations.extend(content.get('verbose', []))

        for speech in main_explanations:
            self.color.print(speech[0], 'lred')
            for meaning in speech[1:]:
                self.color.print(
                    '{text}'.format(text=meaning[0]),
                    'org',
                    indent=2
                )
                for sentence in meaning[1:]:
                    if sentence:
                        print(' ' * 4, end='')
                        for i, s in enumerate(sentence.split('*')):
                            self.color.print(
                                s,
                                'lindigo' if i % 2 else 'indigo',
                                end=''
                            )
                        print()
        print()

    def query(self, word: str):
        webpage = self._get_raw(word)
        data = BeautifulSoup(webpage, "html.parser")
        content = {}

        # handle record.word
        try:
            content['word'] = data.find('span', id='term').text
        except AttributeError:
            raise NotFoundError(word)

        # handle pronounce
        pronu_value = data.find('span', id='pronunciation_pos').text
        if pronu_value:
            content['pronounce'] = []
            for match in re.finditer('(\w+)(\[.*?\])', pronu_value):
                content['pronounce'].append(match.group(1, 2))

        # handle sound
        pronu_sound = data.find(class_='proun_sound')
        if pronu_sound:
            content['sound'] = [
                ('mp3', pronu_sound.find(
                        class_='source',
                        attrs={'data-type': 'audio/mpeg'}
                    ).attrs['data-src']),
                ('ogg', pronu_sound.find(
                        class_='source',
                        attrs={'data-type': 'audio/ogg'}
                    ).attrs['data-src']),
            ]

        # Handle explain
        main_explanations = data.find(
            class_='dd algo explain mt-20 lst DictionaryResults'
        )
        if main_explanations:
            main_explanations = itertools.zip_longest(
                main_explanations.find_all(class_='compTitle mb-10'),
                main_explanations.find_all(
                    class_='compArticleList mb-15 ml-10',
                )
            )
        else:
            main_explanations = ""

        content['explain'] = []
        for part_of_speech, meaning in main_explanations:
            node = [part_of_speech.text] if part_of_speech else ['']

            for item in meaning.find_all('li', class_='ov-a'):
                pack = [item.find('h4').text]

                for example in (
                    tag for tag in item.find_all('span')
                    if 'line-height: 17px;' not in tag['style']
                ):
                    sentence = ''

                    for w in example.contents:
                        if w.name == 'b':
                            sentence += '*' + w.text + '*'
                        else:
                            try:
                                sentence += w
                            except:
                                pass

                    pack.append((sentence.strip()))
                node.append(pack)
            content['explain'].append(node)

            # verbose info
            part_of_speech_list, meaning_list = [], []
            content['verbose'] = []

            variation_explanations = data.find(
                class_='dd algo variation fst DictionaryResults'
            )
            if variation_explanations:
                part_of_speech_list.extend(
                    variation_explanations.find_all(class_='compTitle')
                )
                meaning_list.extend(
                    variation_explanations.find_all(class_='compArticleList')
                )

            additional_explanations = data.find(
                class_='dd algo othersNew lst DictionaryResults'
            )
            if additional_explanations:
                part_of_speech_list.extend(
                    additional_explanations.find_all(class_='compTitle mt-26')
                )
                meaning_list.extend(
                    additional_explanations.find_all(class_='compArticleList')
                )

            more_explanations = itertools.zip_longest(
                part_of_speech_list, meaning_list
            )

            for part_of_speech, meaning in more_explanations:
                node = [part_of_speech.text] if part_of_speech else ['']

                if meaning:
                    for item in meaning.find_all('li', class_='ov-a'):
                        pack = [item.find('h4').text]

                        for example in (
                            tag for tag in item.find_all('span')
                            if 'line-height: 17px;' not in tag['style']
                        ):
                            sentence = ''

                            for w in example.contents:
                                if w.name == 'b':
                                    sentence += '*' + w.text + '*'
                                else:
                                    try:
                                        sentence += w
                                    except:
                                        pass

                            pack.append((sentence.strip()))
                        node.append(pack)
                content['verbose'].append(node)

        record = Record(
                    word=word,
                    content=json.dumps(content),
                    source=self.provider,
                 )
        return record
