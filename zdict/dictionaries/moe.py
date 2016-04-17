import json

from zdict.dictionary import DictBase
from zdict.exceptions import QueryError, NotFoundError
from zdict.models import Record


class MoeDict(DictBase):

    API = 'https://www.moedict.tw/uni/{word}'

    @property
    def provider(self):
        return 'moe'

    @property
    def title(self):
        return '萌典'

    def _get_url(self, word) -> str:
        return self.API.format(word=word)

    def show(self, record: Record):
        content = json.loads(record.content)

        # print word
        self.color.print(content.get('title', ''), 'yellow')

        for word in content.get('heteronyms', ''):

            # print pronounce
            for key, display in (
                ('bopomofo', '注音'),
                ('bopomofo2', '注音二式'),
                ('pinyin', '漢語拼音')
            ):
                self.color.print(display, end='')
                self.color.print(
                    '[' + word.get(key, '') + ']',
                    'lwhite',
                    end=' ',
                )
            print()
            print()

            # print explain
            for count, explain in enumerate(word.get('definitions', '')):

                self.color.print(
                    '{order}. {text}'.format(
                        order=count+1,
                        text=explain.get('def', '')
                    ),
                )

                if explain.get('synonyms'):
                    self.color.print(
                        '同義詞: {text}'.format(text=explain['synonyms']),
                        'magenta',
                        indent=2,
                    )

                if explain.get('antonyms'):
                    self.color.print(
                        '反義詞: {text}'.format(text=explain['antonyms']),
                        'magenta',
                        indent=2,
                    )

                for example in explain.get('example', ''):
                    self.color.print(
                        example,
                        'indigo',
                        indent=2,
                    )

                for quote in explain.get('quote', ''):
                    self.color.print(
                        '[引用] {text}'.format(text=quote),
                        'green',
                        indent=2,
                    )

                print()

    def query(self, word: str):
        try:
            content = self._get_raw(word)
        except QueryError as exception:
            raise NotFoundError(exception.word)

        record = Record(
                    word=word,
                    content=content,
                    source=self.provider,
                 )

        return record
