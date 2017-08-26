import json

from zdict.dictionary import DictBase
from zdict.exceptions import NotFoundError
from zdict.models import Record


# The daily request limit is 1,000,000 characters. The monthly limit is 10,000,000 characters.
API_KEY = 'trnsl.1.1.20170826T075621Z.6dfcaff242c6caa8.e2b9cf136d451d9d6eb69516ec97b827e8c8229b'


# Change `Template` to the name of new dictionary. like xxxDict.
class YandexDict(DictBase):
    """
    Docs:

    * https://tech.yandex.com/translate/
    * https://tech.yandex.com/dictionary/

    """

    # Change the url below to the API url of the new dictionary.
    # Need to keep the `{word}` for `_get_url()` usage.
    # TODO: support different translate direction
    # TODO: use Dictionary API
    API = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key={api_key}&text={word}&lang=ru-en'

    @property
    def provider(self):
        return 'yandex'

    @property
    def title(self):
        return 'Yandex Translate'

    def _get_url(self, word) -> str:
        return self.API.format(api_key=API_KEY, word=word)

    def show(self, record: Record):
        content = json.loads(record.content)

        self.color.print(record.word, 'yellow')
        print()

        for index, data in enumerate(content['text']):
            self.color.print('{}. {}'.format(index+1, data), 'org')

        print()

    def query(self, word: str):
        content = self._get_raw(word)
        content_json = json.loads(content)

        if not content_json['code'] != '200':
            # TODO: handle response codes for different situation
            raise NotFoundError(word)

        record = Record(
            word=word,
            content=content,
            source=self.provider,
         )

        return record
