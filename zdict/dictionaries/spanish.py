import json

from bs4 import BeautifulSoup

from zdict.dictionary import DictBase
from zdict.exceptions import NotFoundError
from zdict.models import Record


# [TODO]
#
# * let user choose en <-> spanish
# * some word's webpage use different CSS class ... (e.g. yo)
# * make code much more readable


class SpanishDict(DictBase):
    '''
    Tested words : ('soy', 'manzana', 'python', 'perdón')
    '''

    API = 'http://www.spanishdict.com/translate/{word}'

    @property
    def provider(self):
        return 'spanish'

    @property
    def title(self):
        return 'SpanishDict'

    def _get_url(self, word) -> str:
        return self.API.format(word=word)

    def show(self, record: Record):
        content = json.loads(record.content)

        self.color.print(content['word'], 'yellow')

        explains = content.get('explains')

        for data in explains:

            self.color.print(data[0], 'lwhite')     # speech

            for explain in data[1]:
                self.color.print(explain[0], 'lred')    # category
                for sentence in explain[1]:
                    self.color.print(
                        '{text}'.format(text=sentence[0]),
                        'org',
                        indent=2
                    )
                    if len(sentence) > 2:
                        self.color.print(
                            '{text}'.format(text=sentence[1]),
                            'lindigo',
                            indent=4
                        )
                        self.color.print(
                            '{text}'.format(text=sentence[2]),
                            'indigo',
                            indent=4
                        )
        print()

    def query(self, word: str):
        webpage = self._get_raw(word)
        data = BeautifulSoup(webpage, "html.parser")
        content = {}

        # word can be existing in both English & Spanish
        # choose English to Spanish here
        # 'translat-en' for English to Spanish
        # 'translat-es' for Spanish to English
        translate_en = data.find('div', id='translate-es')
        if translate_en:
            data = translate_en

        card = data.find('div', attrs={'class': 'card'})
        entry = card.find(
            # just get the first one
            attrs={'class': 'dictionary-entry'}
        )

        if not entry:
            raise NotFoundError(word)

        content['explains'] = []

        word_element = card.find(attrs={'class': 'source-text'})
        if word_element:
            content['word'] = word_element.text

        pattern1 = {'class': 'dictionary-neodict-indent-1'}
        pattern2 = {'class': 'dictionary-neodict-indent-2'}
        pattern3 = {'class': 'dictionary-neodict-indent-3'}
        pattern_order = {'class': 'dictionary-neodict-translation'}
        pattern_example = {'class': 'dictionary-neodict-example'}
        pattern1_en = {'class': 'dictionary-neoharrap-indent-1'}
        pattern2_en = {'class': 'dictionary-neoharrap-indent-2'}
        pattern_order_en = {'class': 'dictionary-neoharrap-translation'}

        speeches = card.find_all(attrs={'class': 'part_of_speech'})

        for (speech, category) in zip(
            speeches,
            entry.find_all(attrs=pattern1) or entry.find_all(attrs=pattern1_en)
        ):
            result = []
            content['explains'].append([speech.text, result])
            context = category.find(attrs={'class': 'context'}).text
            explains = []

            for explain in (category.find_all(attrs=pattern2) or
                            category.find_all(attrs=pattern2_en)):

                orders = (explain.find_all(attrs=pattern_order) or
                          explain.find_all(attrs=pattern_order_en))

                if orders:
                    # e.g.
                    #
                    #   ('a. forgiveness', 'b. pardon (law)')
                    #
                    indices = tuple(
                        map(
                            lambda x: x.text.replace('\xa0', ' ').strip(),
                            orders
                        )
                    )
                else:
                    continue

                examples = explain.find_all(attrs=pattern3)

                for (example, index) in zip(examples, indices):
                    t = tuple(example.find(attrs=pattern_example))
                    (spanish, english) = (t[0].text, t[2].text)
                    explains.append((index, spanish, english))

                if (not examples) and (len(indices) > 0):
                    for index in indices:
                        explains.append((index,))

            result.append([context, explains])

        record = Record(
            word=word,
            content=json.dumps(content),
            source=self.provider,
        )

        return record
