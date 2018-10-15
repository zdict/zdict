import json

from bs4 import BeautifulSoup

from zdict.dictionary import DictBase
from zdict.exceptions import NotFoundError
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

        # Get the first definition string from json.
        definition = content['en'][0]['definitions'][0]['definition']

        # Clean the definition string from html tags.
        definition = BeautifulSoup(definition, "lxml").text

        # Render the output.
        self.color.print(record.word, 'yellow')
        self.color.print(
            definition,
            'org',
            indent=2,
        )

    def query(self, word: str):
        content = self._get_raw(word)

        record = Record(
            word=word,
            content=content,
            source=self.provider,
        )

        return record
