import json

from zdict.dictionary import DictBase
from zdict.exceptions import NotFoundError
from zdict.models import Record


class UrbanDict(DictBase):

    API = 'http://api.urbandictionary.com/v0/define?term={word}'

    @property
    def provider(self):
        return 'urban'

    @property
    def title(self):
        return 'Urban Dictionary'

    def _get_url(self, word) -> str:
        return self.API.format(word=word)

    def show(self, record: Record):
        content = json.loads(record.content)

        data = content['list'][0]

        # print word
        self.color.print(data.get('word', ''), 'yellow')

        self.color.print(
            data.get('definition', ''),
            'org',
            indent=2,
        )

        for example in data.get('example', '').split('\n'):
            self.color.print(
                example,
                'indigo',
                indent=2,
            )

        print()

    def query(self, word: str):
        content_str = self._get_raw(word)
        content_dict = json.loads(content_str)

        if content_dict['list'] == []:
            raise NotFoundError(word)

        record = Record(
            word=word,
            content=content_str,
            source=self.provider,
        )

        return record
