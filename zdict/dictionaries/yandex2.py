import json

from zdict.dictionary import DictBase
from zdict.exceptions import NotFoundError, QueryError
from zdict.models import Record
from zdict.utils import Color
import random

API_KEY = 'trnsl.1.1.20170826T075621Z.' \
          '6dfcaff242c6caa8.e2b9cf136d451d9d6eb69516ec97b827e8c8229b'

class YandexDictResp1Res:
    def __init__(self, json_obj):
        self.content = json_obj

    def print_using_color(self, color: Color):
        def print_translation(tr):
            color.print(tr['text'], 'lred', end=' ')
            color.print('(%s)' % tr['pos']['text'])
        def print_examples(ex):
            def print_example_sentence(s, indent=0):
                color.print_with_highlight(s, r'<([a-zA-Zа-я]+)>', 'indigo', 'lindigo', indent=indent)
            print_example_sentence('┌ %s' % ex['src'], 1)
            print_example_sentence('└ %s' % ex['dst'], 1)
        r = self.content
        tr = r['translation']
        if not tr or 'text' not in tr:
            print()
            return
        print_translation(tr)
        for ex in random.sample(r['examples'], min(3, len(r['examples']))):
            print_examples(ex)
        color.print()

    def is_valid(self):
        return 'text' in self.content['translation']

class YandexDictResp1:
    def __init__(self, json_obj):
        self.content = json_obj

    def print_using_color(self, color: Color):
        result = self.content['result']
        if len(result) == 0:
            raise ValueError

        color.print(result[0]['text'], 'yellow')
        lst = [YandexDictResp1Res(x) for x in self.content['result']]
        lst = [x for x in lst if x.is_valid()]
        for i, x in enumerate(lst):
            color.print('%d. ' % (i+1), 'lred', end=' ')
            x.print_using_color(color)

class YandexDict(DictBase):
    HOMEPAGE_URL = "https://dictionary.yandex.com/"
    API = 'https://dictionary.yandex.net/dicservice.json/queryCorpus?ui=en&srv=tr-text&type&lang=ru-en&src={word}&dst'

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
        return 'yandex2'

    @property
    def title(self):
        return 'Yandex Translate v2'

    def _get_url(self, word) -> str:
        return self.API.format(api_key=API_KEY, word=word)

    def show(self, record: Record):
        content = json.loads(record.content)
        try:
            YandexDictResp1(content).print_using_color(self.color)
        except ValueError as e:
            self.color.print("No entries found\n")

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
