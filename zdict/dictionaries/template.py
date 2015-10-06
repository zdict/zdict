import json

from bs4 import BeautifulSoup

from ..dictionary import DictBase
from ..exceptions import NotFoundError
from ..models import Record


# Change `Template` to the name of new dictionary. like xxxDict.
class TemplateDict(DictBase):

    # Change the url below to the API url of the new dictionary.
    # Need to keep the `{word}` for `_get_url()` usage.
    API = 'https://tw.dictionary.search.yahoo.com/search?p={word}'

    @property
    def provider(self):
        # Change `template` to the short name of the new dictionary.
        return 'template'


    def _get_url(self, word) -> str:
        return self.API.format(word=word)


    def show(self, record: Record, verbose=False):
        content = json.loads(record.content)

        # Use `self.color.print()` to render the output.
        # TODO: Add the API doc of the `color.print()`
        print()

        if verbose:
            try:
                # Get the addtional information if it exists.
                pass
            except:
                return
            else:
                # Define how to print the additional information
                print()


    def query(self, word: str, timeout: float, verbose=False):
        webpage = self._get_raw(word, timeout)
        data = BeautifulSoup(webpage, "html.parser")
        content = {}

        # Parse `data` and fill the information you need into `content`
        #
        # Use
        # ```
        # except AttributeError:
        #    raise NotFoundError(word)
        # ```
        # while the word users try to query is not found on this dictionary.

        if verbose:
            # Store the additonal information for the verbose option.
            pass

        record = Record(word=word,
                        content=json.dumps(content),
                        source=self.provider,
                 )

        return record
