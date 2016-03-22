import json

from ..dictionary import DictBase
from ..exceptions import NotFoundError
from ..models import Record


class JishoDict(DictBase):

    # Change the url below to the API url of the new dictionary.
    # Need to keep the `{word}` for `_get_url()` usage.
    API = 'http://jisho.org/api/v1/search/words?keyword={word}'

    @property
    def provider(self):
        # Change `template` to the short name of the new dictionary.
        return 'Jisho'


    def _get_url(self, word) -> str:
        return self.API.format(word=word)


    def show(self, record: Record, verbose=False):
        content = json.loads(record.content)

        #for data in content['data']:
        for data in (content['data'][0],):

            # print word
            reading = data['japanese'][0].get('reading', '')
            word = data['japanese'][0].get('word', '')

            if reading:
                self.color.print(reading, 'lyellow')

            if word:
                self.color.print(word, 'yellow')
            print()

            for idx, sense in enumerate(data['senses'], 1):

                if sense['parts_of_speech']:
                    self.color.print(', '.join(sense['parts_of_speech']), 'lred')

                self.color.print(str(idx) + '. ' + '; '.join(sense['english_definitions']), 'lgreen', indent=2)

                if sense['see_also']:
                    self.color.print('See also ' + ', '.join(sense['see_also']), 'blue', indent=4)
                if sense['restrictions']:
                    self.color.print('Only to ' + ', '.join(sense['restrictions']), 'blue', indent=4)
        print()

        # there are other forms for this word.
        if len(data['japanese']) > 1:

            self.color.print('Other forms')
            word_forms = []
            for word_form in data['japanese'][1:]:

                reading = word_form.get('reading', '')
                word = word_form.get('word', '')
                word_forms.append('{word}[{reading}]'.format(word=word, reading=reading))

            self.color.print(', '.join(word_forms), 'yellow', indent=2)

    def query(self, word: str, timeout: float, verbose=False):
        content = self._get_raw(word, timeout)

        content_json = json.loads(content)
        if not content_json['data']:
            raise NotFoundError(word)

        record = Record(
                    word=word,
                    content=content,
                    source=self.provider,
                 )

        return record
