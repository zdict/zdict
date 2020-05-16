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
                for t in explain[1]:
                    # t = (index, (sentence, sentence, ...))
                    self.color.print(  # index
                        '{text}'.format(text=t[0]),
                        'org',
                        indent=2
                    )
                    if len(t) > 1:
                        for sentence in t[1]:
                            # sentence = (spanish, english)
                            self.color.print(
                                '{text}'.format(text=sentence[0]),
                                'lindigo',
                                indent=4
                            )
                            self.color.print(
                                '{text}'.format(text=sentence[1]),
                                'indigo',
                                indent=4
                            )
        print()

    def query(self, word: str):
        webpage = self._get_raw(word)
        soup = BeautifulSoup(webpage, "html.parser")
        content = {}

        en_css = "#dictionary-neodict-en"
        es_css = "#dictionary-neodict-es"
        card = soup.select_one(en_css) or soup.select_one(es_css)
        if card is None:
            raise NotFoundError(word)

        word_css = "div > div:nth-child(1) > span"
        word_element = card.select_one(word_css)
        if word_element is None:
            raise NotFoundError(word)
        content['word'] = word_element.text

        '''
        COPULAR VERB  # speech
            # categories_card
            1. (used to express a permanent quality)  # category_text
                # explanation
                a. ser  # index
                # examples
                    # example
                    The ocean is blue.
                    El océano es azul.
            2. (used to express a temporary state)
                a. estar
                    I'm not in a good mood today.
                    Hoy no estoy de buen humor.

                    The sky is cloudy.
                    El cielo está nublado.
        ... (Another speech if it has.)
        '''
        speech_pattern = "div > div:nth-child(2)"
        # "#dictionary-neodict-en > div > div:nth-child(2)"

        # Start to grab
        content['explains'] = []
        speech = card.select_one(speech_pattern)
        while speech:
            result = []
            speech_text, categories_card = speech.children
            speech_text_element = speech_text.find(['a', 'span'])
            content['explains'].append([speech_text_element.text, result])

            for category in categories_card.children:
                category_text_element, explanations_card = category.children
                category_text = category_text_element.text

                explains = []
                for explanation in explanations_card.children:
                    for _ in explanation.children:
                        index_elements, examples = (
                            _.contents[:-1], _.contents[-1]
                        )
                        index = ' '.join(
                            [
                                _.text.strip() for _ in index_elements
                                if _ != ' '
                            ]
                        )

                        if (not examples) and index:
                            explains.append((index,))
                            continue

                        sentences = []
                        for example in examples:
                            t = example.find_all()
                            # Should be only 3 elements
                            # [text, —,  text]
                            '''
                            When Spanish => English, it will show Spanish first
                            When English => Spanish, it will show English first
                            So, the variables below are not definitely
                            '''
                            sentences.append((t[0].text, t[2].text))
                        explains.append((index, sentences))

                result.append([category_text, explains])
            speech = speech.next_sibling

        record = Record(
            word=word,
            content=json.dumps(content),
            source=self.provider,
        )

        return record
