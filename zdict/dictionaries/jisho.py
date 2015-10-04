import json

from ..dictionary import DictBase
from ..exceptions import NotFoundError
from ..models import Record


class JishoDict(DictBase):

    # Change the url below to the API url of the new dictionary.
    # Need to keep the `{word}` for `_get_url()` usage.
    API = 'http://jisho.org/api/v1/search/words?keyword={word}'

    @property
    def provider(self):
        # Change `template` to the short name of the new dictionary.
        return 'Jisho'


    def _get_url(self, word) -> str:
        return self.API.format(word=word)


    def show(self, record: Record, verbose=False):
        content = json.loads(record.content)

        self.color.print('This dictionary is still WIP', 'lred')

        #for data in content['data']:
        for data in (content['data'][0],):

            # print word
            self.color.print(data['japanese'][0]['reading'], 'lyellow')

            word = data['japanese'][0].get('word', '')

            if word:
                self.color.print(word, 'green', indent=2)

            for sense in data['senses']:
                self.color.print(';'.join(sense['english_definitions']), 'green', indent=2)

        print()


    def query(self, word: str, timeout: float, verbose=False):
        content = self._get_raw(word, timeout)

        record = Record(
                    word=word,
                    content=content,
                    source=self.provider,
                 )

        return record
