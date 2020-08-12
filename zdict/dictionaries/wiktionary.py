import json

from bs4 import BeautifulSoup

from zdict.dictionary import DictBase
from zdict.exceptions import NotFoundError, QueryError
from zdict.models import Record


class WiktionaryDict(DictBase):

    HOMEPAGE_URL = "https://en.wiktionary.org/"
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

        # Render the output.
        self.color.print(record.word, 'lyellow')

        if self.args.verbose:
            for d in content:
                self.color.print(d['part_of_speech'], 'yellow', indent=2)
                for i, defin in enumerate(d['definitions']):
                    self.color.print("{}. {}".format(i+1, defin['definition']),
                                     'org', indent=4)
                    try:
                        defin['examples']
                    except KeyError:
                        pass
                    else:
                        # self.color.print(f"Examples:", 'lindigo', indent=6)
                        for example in defin['examples']:
                            self.color.print(example, 'indigo', indent=6)
        else:
            d = content[0]
            self.color.print(d['part_of_speech'], 'yellow', indent=2)
            self.color.print(d['definitions'][0]['definition'],
                             'org',
                             indent=4)

    def query(self, word: str):
        try:
            content = self._get_raw(word)
        except QueryError as exception:
            raise NotFoundError(exception.word)

        content = json.loads(content)

        try:
            # Get the first definition string from JSON.
            content = content['en']
        except KeyError:
            # API can return JSON that does not contain 'en' language.
            raise NotFoundError(word)

        # Define a list that will be used to create a Record.
        r_content = []

        # For every part of speech append r_content corresponding list.
        for i, d in enumerate(content):
            # Add what part of speech current definitions refers to.
            r_content.append({'part_of_speech': d['partOfSpeech']})

            # Create a list that will store english_definitions
            # of the current part of speech.
            r_content[i]['definitions'] = []

            for j, d2 in enumerate(d['definitions']):
                # Parse definition and append definitions list.
                definition = BeautifulSoup(d2['definition'],
                                           "html.parser").text
                r_content[i]['definitions'].append({'definition': definition})

                # If API provides examples for the current definition
                # create a new list and append them.
                try:
                    d2['examples']
                except KeyError:
                    pass
                else:
                    r_content[i]['definitions'][j]['examples'] = []
                    for ex in d2['examples']:
                        ex = BeautifulSoup(ex, "html.parser").text
                        r_content[i]['definitions'][j]['examples'].append(ex)

        record = Record(
            word=word,
            content=json.dumps(r_content),
            source=self.provider,
        )

        return record
