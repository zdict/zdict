import json
from random import randint

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

        # hybrid way to select showing answers
        # first 3 answers + random 1 answer from rest of them
        answers = content['list'][:3]
        answers_length = len(content['list'])
        if answers_length > 3:
            answers.append(content['list'][randint(3, answers_length-1)])

        for data in answers:
            word = data.get('word', '')
            if "</h1>" in word:   # there are some wierd case, e.g. "asdasd"
                continue

            # print word
            self.color.print(word, 'yellow')

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
