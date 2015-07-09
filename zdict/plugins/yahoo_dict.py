import itertools
import json
import re

from bs4 import BeautifulSoup

from ..dictionaries import DictBase
from ..exceptions import NotFoundError
from ..models import Record


class YahooDict(DictBase):

    API = 'https://tw.dictionary.yahoo.com/dictionary?p={word}'

    @property
    def provider(self):
        return 'yahoo'

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
        explain = content.get('explain')
        for speech in explain:
            self.color.print(speech[0], 'lred')
            for meaning in speech[1:]:
                self.color.print(
                    '{text}'.format(text=meaning[0]),
                    'org',
                    indent=2
                )
                for (english, chinese) in meaning[1:]:
                    if english:
                        print(' ' * 4, end='')
                        for i, s in enumerate(english.split('*')):
                            self.color.print(
                                s,
                                'lindigo' if i == 1 else 'indigo',
                                end=''
                            )
                        print()

                    if chinese:
                        self.color.print(chinese, 'green', indent=4)
        print()

    def query(self, word: str, timeout: float, verbose=False):
        webpage = self._get_raw(word, timeout)
        data = BeautifulSoup(webpage)
        content = {}

        # handle record.word
        try:
            content['word'] = data.find('span', id='term').text
        except AttributeError:
            raise NotFoundError(word)

        # handle pronounce
        pronu_value = data.find('span', id='pronunciation_pos').text
        if pronu_value:
            p = re.compile('(\w+)(\[.*\])')
            content['pronounce'] = []
            for pronu in pronu_value.split():
                m = p.match(pronu)
                content['pronounce'].append(m.group(1, 2))

        # handle sound
        # looks like the sound had been removed. 2015/05/26
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

        # handel explain
        if verbose:
            search_exp = data.find_all(class_='dd algo lst DictionaryResults')
        else:
            search_exp = data.find(
                class_='dd algo mt-20 lst DictionaryResults'
            )
            search_exp = itertools.zip_longest(
                search_exp.find_all(class_='compTitle mb-10'),
                search_exp.find_all(class_='compArticleList mb-15 ml-10')
            )

        content['explain'] = []
        for part_of_speech, explain in search_exp:
            node = [part_of_speech.text] if part_of_speech else ['']

            for item in explain.find_all('li', class_='ov-a'):
                pack = [item.find('h4').text]
                for example in item.find_all('span', id='example'):
                    sentence = ''
                    translation = ''

                    for w in example.contents:
                        if w.name == 'b':
                            sentence += '*' + w.text + '*'
                        elif w.name == 'span':
                            translation = w.text
                        else:
                            try:
                                sentence += w
                            except:
                                pass

                    pack.append((sentence.strip(), translation.strip()))
                node.append(pack)
            content['explain'].append(node)

        record = Record(
                    word=word,
                    content=json.dumps(content),
                    source=self.provider,
                 )
        return record
