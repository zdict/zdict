import json

from bs4 import BeautifulSoup

from zdict.dictionary import DictBase
from zdict.exceptions import NotFoundError, QueryError
from zdict.models import Record


class WiktionaryDict(DictBase):

    API = 'https://en.wiktionary.org/api/rest_v1/page/definition/{word}'

    @property
    def provider(self):
        return 'wiktionary'

    @property
    def title(self):
        return 'Wiktionary'

    def _get_url(self, word) -> str:
        return self.API.format(word=word)

    def show(self, record: Record):
        content = json.loads(record.content)

        # Render the output.
        self.color.print(record.word, 'yellow')
        self.color.print(
            content['definition'],
            'org',
            indent=2,
        )

    def query(self, word: str):
        try:
            content = self._get_raw(word)
        except QueryError as exception:
            raise NotFoundError(exception.word)

        content = json.loads(content)

        try:
            # Get the first definition string from JSON.
            definition = content['en'][0]['definitions'][0]['definition']
        except KeyError as exception:
            # API can return JSON that does not contain 'en' language.
            raise NotFoundError(word)
        else:
            # Clean the definition string from HTML tags.
            definition = BeautifulSoup(definition, "html.parser").text
            content = {}
            content['definition'] = definition

        record = Record(
            word=word,
            content=json.dumps(content),
            source=self.provider,
        )

        return record
