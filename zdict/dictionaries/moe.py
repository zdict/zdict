import json
import unicodedata  # to detect Unicode category

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
                        order=count + 1,
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


def is_other_format(char):
    return unicodedata.category(char) != 'Cf'


def remove_cf(data):
    return ''.join(filter(is_other_format, data))


def clean(data, clean_cf=False):
    '''
    Clean the word segmentation

    remove "`~" and things in Unicode 'Cf' category
    '''
    data = data.translate(str.maketrans('', '', '`~'))
    if clean_cf:
        return remove_cf(data)
    else:
        return data


class MoeDictTaiwanese(DictBase):

    API = 'https://www.moedict.tw/t/{word}.json'

    @property
    def provider(self):
        return 'moe-taiwanese'

    @property
    def title(self):
        return '萌典（臺）'

    def _get_url(self, word) -> str:
        return self.API.format(word=word)

    def show(self, record: Record):
        content = json.loads(record.content)

        # print word
        self.color.print(clean(content.get('t', '')), 'yellow')

        for word in content.get('h', ''):

            # print pronounce
            for key, display in (
                # TODO: where is bopomofo ?
                ('T', '臺羅拼音'),      # Tailo
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
            for count, explain in enumerate(word.get('d', '')):

                self.color.print('{order}. '.format(order=count + 1), end='')
                type = clean(explain.get('type', ''))
                if type:
                    self.color.print(
                        '[' + type + ']',
                        'lgreen',
                        end=' ',
                    )

                self.color.print(clean(explain.get('f', '')), end='')

                for example in explain.get('e', ''):
                    self.color.print(
                        clean(example, True),
                        'indigo',
                        indent=2,
                    )

                print()

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
