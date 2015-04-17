import json

from bs4 import BeautifulSoup

from ..dictionarys import DictBase
from ..exceptions import NotFoundError, QueryError
from ..models import Record


class yDict(DictBase):
    API = 'https://tw.dictionary.yahoo.com/dictionary?p={word}'

    def _get_prompt(self) -> str:
        return '[yDict]: '

    def _get_url(self, word) -> str:
        return self.API.format(word=word)

    def query(self, word: str, verbose=False):
        '''
        :param word: look up word
        :param verbose: verbose mode flag
        '''

        keyword = word.lower()

        try:
            record = Record.get(word=keyword, source=self.provider)
        except Record.DoesNotExist as e:
            record = Record(word=keyword, source=self.provider, content=None)
        else:
            return record

        data = BeautifulSoup(self._get_raw(word))
        content = {}
        # handle record.word
        try:
            content['word'] = data.find('span', class_='yschttl').text
        except AttributeError:
            raise NotFoundError(word)
        # handle pronounce
        pronu_value = data.find_all('span', class_='proun_value')
        if pronu_value:
            content['pronounce'] = [
                ('KK', pronu_value[0].text),
                ('DJ', pronu_value[1].text),
            ]
        # handle sound
        pronu_sound = data.find(class_='proun_sound')
        if pronu_sound:
            content['sound'] = [
                ('mp3', pronu_sound.find(
                        class_='source',
                        attrs={'data-type': 'audio/mpeg'}
                    ).attrs['data-src']
                ),
                ('ogg', pronu_sound.find(
                        class_='source',
                        attrs={'data-type': 'audio/ogg'}
                    ).attrs['data-src']
                ),
            ]

        if verbose:
            search_exp = data.find_all(class_='explanation_pos_wrapper')
        else:
            search_exp = data.find(class_='result_cluster_first').find_all(class_='explanation_pos_wrapper')

        content['explain'] = []
        for explain in search_exp:
            node = [explain.h5.text]

            for item in explain.ol.find_all('li'):
                pack = [item.find('p', class_='explanation').text]
                for sample in item.find_all('p', class_='sample'):
                    samp = sample.find_all('samp')
                    pack.append((
                        ''.join([
                            ('*{}*'.format(tag.text) if tag.name == 'b' else tag)
                            for tag in samp[0].contents
                        ]),
                        samp[1].text
                    ))

                node.append(pack)

            content['explain'].append(node)

        record.content = json.dumps(content)
        record.save(force_insert=True)  # using force_insert for CompositeKey
        return record

    @property
    def provider(self):
        return 'yahoo'

