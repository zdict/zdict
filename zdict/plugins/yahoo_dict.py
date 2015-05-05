import json

from ..dictionaries import DictBase
from ..exceptions import NotFoundError
from ..models import Record


class YahooDict(DictBase):

    API = 'https://tw.dictionary.yahoo.com/dictionary?p={word}'

    @property
    def provider(self):
        return 'yahoo'

    def show(self, record: Record):
        content = json.loads(record.content)
        # print word
        self.color.print(content['word'], 'yellow')
        # print pronounce
        for k, v in content.get('pronounce', []):
            self.color.print(k, end='')
            self.color.print(v, 'lwhite', end=' ')
        print()
        # print explain
        explain = content.get('explain')
        for speech in explain:
            self.color.print(speech[0], 'lred')
            for index, meaning in enumerate(speech[1:], start=1):
                self.color.print(
                    '{num}. {text}'.format(num=index, text=meaning[0]),
                    'org',
                    indent=2
                )
                for sentence in meaning[1:]:
                    print(' ' * 4, end='')
                    for i, s in enumerate(sentence[0].split('*')):
                        self.color.print(
                            s,
                            'lindigo' if i == 1 else 'indigo',
                            end=''
                        )
                    print()
                    self.color.print(sentence[1], 'green', indent=4)
        print()

    def _get_prompt(self) -> str:
        return '[zDict]: '

    def _get_url(self, word) -> str:
        return self.API.format(word=word)

    @property
    def selectors(self):
        return [
            {
                'li.result_cluster_first': [
                    'span.yschttl',
                    'span.proun_wrapper',
                    'ul.explanation_wrapper',
                ],
            },
            'li.result_cluster ul.explanation_wrapper',
        ]
