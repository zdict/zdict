import json

from zdict.dictionary import DictBase
from zdict.exceptions import NotFoundError, QueryError
from zdict.models import Record


# The daily request limit is 1,000,000 characters
# The monthly limit is 10,000,000 characters
API_KEY = 'trnsl.1.1.20170826T075621Z.' \
          '6dfcaff242c6caa8.e2b9cf136d451d9d6eb69516ec97b827e8c8229b'


class YandexDict(DictBase):
    """
    Docs:

    * https://tech.yandex.com/translate/
    * https://tech.yandex.com/dictionary/

    """

    HOMEPAGE_URL = "https://translate.yandex.com/"
    # TODO: support different translate direction
    # TODO: use Dictionary API
    API = 'https://translate.yandex.net/api/v1.5/tr.json/translate?' \
          'key={api_key}&text={word}&lang=ru-en'

    status_code = {
        200: 'Operation completed successfully',
        401: 'Invalid API key',
        402: 'Blocked API key',
        404: 'Exceeded the daily limit on the amount of translated text',
        413: 'Exceeded the maximum text size',
        422: 'The text cannot be translated',
        501: 'The specified translation direction is not supported',
    }

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
            self.color.print('{}. {}'.format(index + 1, data), 'org')

        print()

    def query(self, word: str):
        try:
            content = self._get_raw(word)
        except QueryError as exception:
            raise NotFoundError(exception.word)

        content_json = json.loads(content)

        status = content_json.get('code')
        if status != 200:
            # https://tech.yandex.com/translate/doc/dg/reference/translate-docpage/#codes
            message = self.status_code.get(
                status,
                'Some bad thing happened with Yandex'
            )
            print('Yandex: ' + message)
            raise NotFoundError(word)

        record = Record(
            word=word,
            content=content,
            source=self.provider,
        )
        return record
