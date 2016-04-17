import json

from zdict.dictionary import DictBase
from zdict.exceptions import NotFoundError
from zdict.models import Record


class JishoDict(DictBase):

    # Change the url below to the API url of the new dictionary.
    # Need to keep the `{word}` for `_get_url()` usage.
    API = 'http://jisho.org/api/v1/search/words?keyword={word}'

    @property
    def provider(self):
        # Change `template` to the short name of the new dictionary.
        return 'jisho'

    @property
    def title(self):
        return 'Jisho'

    def _get_url(self, word) -> str:
        return self.API.format(word=word)

    def show(self, record: Record):
        content = json.loads(record.content)

        for data in content['data']:
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
                    self.color.print(
                        ', '.join(sense['parts_of_speech']),
                        'lred',
                    )

                self.color.print(
                    "{}. {}".format(
                        idx,
                        '; '.join(sense['english_definitions'])
                    ),
                    'lgreen',
                    indent=2,
                )

                if sense['see_also']:
                    self.color.print(
                        "See also {}".format(', '.join(sense['see_also'])),
                        'blue',
                        indent=4,
                    )
                if sense['restrictions']:
                    self.color.print(
                        "Only to {}".format(', '.join(sense['restrictions'])),
                        'blue',
                        indent=4
                    )

            # there are other forms for this word.
            if len(data['japanese']) > 1:
                self.color.print('Other forms')
                word_forms = []
                for word_form in data['japanese'][1:]:

                    reading = word_form.get('reading', '')
                    word = word_form.get('word', '')
                    word_forms.append(
                        '{word}[{reading}]'.format(word=word, reading=reading)
                    )

                self.color.print(', '.join(word_forms), 'yellow', indent=2)

            if not self.args.verbose:
                break
        print()

    def query(self, word: str):
        content = self._get_raw(word)
        content_json = json.loads(content)
        if not content_json['data']:
            raise NotFoundError(word)

        record = Record(
                    word=word,
                    content=content,
                    source=self.provider,
                 )
        return record
