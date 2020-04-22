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

    API = 'https://www.spanishdict.com/translate/{word}'

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
        card = (
            data.find('div', attrs={'id': 'dictionary-neodict-en'})
            or data.find('div', attrs={'id': 'dictionary-neodict-es'})
        )
        if card is None:
            raise NotFoundError(word)

        word_element = card.find('span', attrs={'class': 'WGK1YbP8'})
        if word_element is None:
            raise NotFoundError(word)
        content['word'] = word_element.text

        '''
        COPULAR VERB  # speech_pattern
            # categories_card_pattern
            1. (used to express a permanent quality)  # category_text_pattern
                a. ser  # explanation_order_pattern, explanation_text_pattern
                    # example_card_pattern
                    The ocean is blue.
                    El océano es azul.
            2. (used to express a temporary state)
                a. estar
                    I'm not in a good mood today.
                    Hoy no estoy de buen humor.

                    The sky is cloudy.
                    El cielo está nublado.
        ... (Another speech pattern if it has.)
        '''
        speech_pattern = {'class': '_2xs-UBSR'}

        categories_card_pattern = {'class': 'FyTYrC-y'}
        category_text_pattern = {'class': '_1vspKqMZ'}

        explanation_order_pattern = {'class': '_1TgBOcUi'}
        explanation_text_pattern = {'class': 'C2TP2MvR'}

        example_card_pattern = {'class': 'FyTYrC-y'}

        # Start to grab
        content['explains'] = []
        speech = card.find(attrs=speech_pattern)
        while speech:
            result = []
            speech_text_element = speech.find(['a', 'span'])
            content['explains'].append([speech_text_element.text, result])

            categories_card = speech.find(attrs=categories_card_pattern)
            for category in categories_card.children:
                category_text_element = category.find(attrs=category_text_pattern)
                category_text = category_text_element.text

                explains = []
                explanation_card = category.find(attrs=example_card_pattern)
                for explanation in explanation_card.children:
                    explanation_orders = explanation.find_all('span', explanation_order_pattern)
                    explanation_texts = explanation.find_all('a', explanation_text_pattern)
                    indices = []
                    if explanation_orders:
                        for explanation_order, explanation_text in zip(explanation_orders, explanation_texts):
                            indices.append(
                                "{}{}".format(
                                    explanation_order.text.strip(),
                                    explanation_text.text.strip()
                                )
                            )
                    else:
                        continue

                    examples = explanation.find_all(attrs=example_card_pattern)
                    for (example, index) in zip(examples, indices):
                        t = example.find_all()
                        # Should be only 4 elements: [(whole sentence), text, —,  text]
                        '''
                        When it's Spanish => English, it will show Spanish first.
                        When it's English => Spanish, it will show English first.
                        So, the variables below are  not definitely.
                        '''
                        (spanish, english) = (t[1].text, t[3].text)
                        explains.append((index, spanish, english))

                    if (not examples) and (len(indices) > 0):
                        for index in indices:
                            explains.append((index,))
                result.append([category_text, explains])
            speech = speech.next_sibling

        record = Record(
            word=word,
            content=json.dumps(content),
            source=self.provider,
        )

        return record
