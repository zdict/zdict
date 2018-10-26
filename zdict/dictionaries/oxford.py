import json
import os
import re

from zdict.constants import BASE_DIR
from zdict.dictionary import DictBase
from zdict.exceptions import NotFoundError, QueryError, APIKeyError
from zdict.models import Record


class OxfordDictionary(DictBase):
    """
    Docs:

    * https://developer.oxforddictionaries.com/documentation/
    """

    KEY_FILE = os.path.join(BASE_DIR, 'oxford.key')

    API = 'https://od-api.oxforddictionaries.com/api/v1/entries/en/{word}'

    # https://developer.oxforddictionaries.com/documentation/response-codes
    status_code = {
        200: 'Success!',
        400: 'The request was invalid or cannot be otherwise served.',
        403: 'The request failed due to invalid credentials.',
        404: 'No entry is found.',
        500: 'Something is broken. Please contact the Oxford Dictionaries '
             'API team to investigate.',
        502: 'Oxford Dictionaries API is down or being upgraded.',
        503: 'The Oxford Dictionaries API servers are up, but overloaded '
             'with requests. Please try again later.',
        504: 'The Oxford Dictionaries API servers are up, but the request '
             'couldn’t be serviced due to some failure within our stack. '
             'Please try again later.'
    }

    @property
    def provider(self):
        return 'oxford'

    @property
    def title(self):
        return 'Oxford Dictionary'

    def _get_url(self, word) -> str:
        return self.API.format(word=word.lower())

    def show(self, record: Record):
        content = json.loads(record.content)

        # results
        for headword in content['results']:
            # word
            self.color.print(headword['word'], 'lyellow')

            for lex_ent in headword['lexicalEntries']:
                # lexical category
                print()
                self.color.print(lex_ent['lexicalCategory'], 'lred', end='')

                # pronunciation
                if 'pronunciations' in lex_ent:
                    pronunciations = [
                        '/' + pronun['phoneticSpelling'] + '/'
                        for pronun in lex_ent['pronunciations']
                    ]
                    pronunciations_str = '  '.join(pronunciations)
                    self.color.print('  ' + pronunciations_str)
                else:
                    print()

                # entry
                idx = 1
                for entry in lex_ent['entries']:
                    for sense in entry['senses']:
                        line_prefix = '{idx}.'.format(idx=idx)
                        self._show_sense(sense, line_prefix)
                        idx += 1

        print()

    def _show_sense(self, sense: dict, prefix='', indent=1):
        print()
        self.color.print(prefix, end=' ', indent=indent)

        # regions
        if 'regions' in sense:
            regions_str = ', '.join(sense['regions'])
            regions_str = '(' + regions_str + ')'
            self.color.print(regions_str, 'yellow', end=' ')

        # register
        if 'registers' in sense:
            registers_str = ', '.join(sense['registers'])
            self.color.print(registers_str, 'red', end=' ')

        # domain
        if 'domains' in sense:
            domains_str = ', '.join(sense['domains'])
            domains_str = '(' + domains_str + ') '
            self.color.print(domains_str, 'green', end='')

        # notes
        if 'notes' in sense:
            notes = [note['text'] for note in sense['notes']]
            notes_str = ', '.join(notes)
            notes_str = '[' + notes_str + '] '
            self.color.print(notes_str, 'magenta', end='')

        # definition
        if 'definitions' in sense:
            definition_str = '. '.join(sense['definitions'])
            print(definition_str)

        # cross ref
        if 'crossReferenceMarkers' in sense:
            xref_marker_str = '. '.join(sense['crossReferenceMarkers'])
            print(xref_marker_str)

        # example
        for example in sense.get('examples', []):
            print()
            print(' ' * (indent + 1), end='  ')
            self.color.print(example['text'], 'indigo', indent=indent+2)

        # subsenses
        if self.args.verbose and 'subsenses' in sense:
            for idx, subsense in enumerate(sense['subsenses'], 1):
                line_prefix = '{prefix}{idx}.'.format(prefix=prefix, idx=idx)
                self._show_sense(subsense, line_prefix, indent=indent + 1)

    def _get_app_key(self):
        """
        Get the app id & key for query

        .. note:: app key storage
            The API key should placed in ``KEY_FILE`` in the ``~/.zdict`` with
            the format::

                app_id,app_key

        .. note:: request limit
            request limit: per minute is 60, per month is 3000.
        """
        if not os.path.exists(self.KEY_FILE):
            self.color.print('You can get an API key by the following steps:',
                             'yellow')
            print('1. Register a developer account at '
                  'https://developer.oxforddictionaries.com/')
            print('2. Get the application id & keys in the `credentials` page')
            print('3. Paste the API key at `{key_file}` in the foramt:'.format(
                key_file=self.KEY_FILE
            ))
            print('     app_id, app_key')
            raise APIKeyError('Oxford: API key not found')

        with open(self.KEY_FILE) as fp:
            keys = fp.read()

        keys = re.sub(r'\s', '', keys).split(',')
        if len(keys) != 2:
            print('The API key should be placed in the format:')
            print('     app_id, app_key')
            raise APIKeyError('Oxford: API key file format not correct.')

        return keys

    def query(self, word: str):
        try:
            app_id, app_key = self._get_app_key()
            content = self._get_raw(word, headers={
                'app_id': app_id,
                'app_key': app_key
            })
        except QueryError as exception:
            msg = self.status_code.get(exception.status_code,
                                       'Some bad thing happened')
            self.color.print('Oxford: ' + msg, 'red')
            raise NotFoundError(exception.word)

        record = Record(
            word=word,
            content=content,
            source=self.provider,
        )
        return record
