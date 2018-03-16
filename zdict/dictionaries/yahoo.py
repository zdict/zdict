import json
import re

from bs4 import BeautifulSoup

from zdict.dictionary import DictBase
from zdict.exceptions import NotFoundError
from zdict.models import Record


class YahooDict(DictBase):

    API = 'https://tw.dictionary.yahoo.com/dictionary?p={word}'

    @property
    def provider(self):
        return 'yahoo'

    @property
    def title(self):
        return 'Yahoo Dictionary'

    def _get_url(self, word) -> str:
        return self.API.format(word=word)

    def show(self, record: Record):
        content = json.loads(record.content)
        getattr(self, 'showv{}'.format(content.get('version', 1)))(content)

    def showv1(self, content):  # legacy
        # print word
        self.color.print(content['word'], 'yellow')

        # print pronounce
        for k, v in content.get('pronounce', []):
            self.color.print(k, end='')
            self.color.print(v, 'lwhite', end=' ')
        print()

        # print explain
        main_explanations = content.get('explain', [])
        if self.args.verbose:
            main_explanations.extend(content.get('verbose', []))

        for speech in main_explanations:
            self.color.print(speech[0], 'lred')
            for meaning in speech[1:]:
                self.color.print(
                    '{text}'.format(text=meaning[0]),
                    'org',
                    indent=2
                )
                for sentence in meaning[1:]:
                    if sentence:
                        print(' ' * 4, end='')
                        for i, s in enumerate(sentence.split('*')):
                            self.color.print(
                                s,
                                'lindigo' if i % 2 else 'indigo',
                                end=''
                            )
                        print()
        print()

    def showv2(self, content):
        # summary
        summary = content['summary']
        # summary > word
        self.color.print(summary['word'], 'yellow')
        # summary > pronounce
        pronounce = summary.get('pronounce', [])
        for k, v in pronounce:
            self.color.print(k, end='')
            self.color.print(v, 'lwhite', end=' ')
        print() if pronounce else None
        # summary > explain
        indent = True
        for (t, s) in summary.get('explain', []):
            if t == 'e':
                self.color.print(s, indent=2 * indent)
                indent = True
            elif t == 'p':
                self.color.print(s, 'lred', end=' ', indent=2 * indent)
                indent = False
        # summary > grammar
        grammar = summary.get('grammar', [])
        print() if grammar else None
        for s in grammar:
            self.color.print(s, indent=2)

        print()
        # explain
        for exp in content.get('explain', []):
            type_ = exp['type']
            if type_ == 'PoS':
                self.color.print(exp['text'], 'lred')
            elif type_ == 'item':
                self.color.print(exp['text'], indent=2)
                sentence = exp.get('sentence')
                if sentence:
                    indent = True
                    for s in sentence:
                        if isinstance(s, str) and s != '\n':
                            self.color.print(s, 'indigo', end='',
                                             indent=indent * 4)
                        elif isinstance(s, list) and s[0] == 'b':
                            self.color.print(s[1], 'lindigo', end='',
                                             indent=indent * 4)
                        elif s == '\n':
                            print()
                            indent = True
                            continue

                        indent = False

        print()

    def query(self, word: str):
        webpage = self._get_raw(word)
        data = BeautifulSoup(webpage, "html.parser")
        content = {}

        # Please bump version if format changed again.
        # the `show` function will act with respect to version number.

        content['version'] = 2

        # Here are details of each version.
        #
        # The original one, in the old era, there isn't any concept of
        # version number:
        # content = {
        #     'word': ...,
        #     'pronounce': ...,
        #     'sound': (optional),
        #     'explain': [...],
        #     'verbose': [...],
        # }
        #
        # Verion 2, yahoo dictionary content is provided by Dy.eye
        # at that moment:
        # content = {
        #     'version': 2,
        #     'summary': {
        #         'word': ...,
        #         'pronounce': [('KK', '...'), (...)],  // optional.
        #                                               // e.g. 'google'
        #         'explain': [...],
        #         'grammar': [(optional)],
        #     },
        #     'explain': [...],
        #     'verbose': [(optional)],
        # }

        def text(x):
            return x.text

        def explain_text(x: 'bs4 node'):
            def f(n):
                def g(ks):
                    if 'pos_button' in ks:
                        return 'p'
                    elif 'dictionaryExplanation' in ks:
                        return 'e'
                    else:
                        return '?'
                ret = list(map(lambda m: (g(m.attrs['class']), m.text), n.select('div')))
                return ret
            return sum(map(f, x.select('ul > li')), [])

        # Construct summary
        summary = content['summary'] = {}
        sum_ = data.select_one('div#web ol.searchCenterMiddle > li > div')
        if not sum_:
            raise NotFoundError(word)
        try:
            ls = sum_.select('> div')
            if len(ls) == 5:
                _, word_, pronoun, _, explain = ls
            elif len(ls) == 4:  # e.g. "hold on"
                _, word_, _, explain = ls
                pronoun = None
            elif len(ls) == 3:  # e.g. "google"
                _, word_, explain = ls
                pronoun = None
            elif len(ls) == 2:  # e.g. "fabor"
                raise NotFoundError(word)

            summary['word'] = word_.find('span').text.strip()
            if pronoun:
                summary['pronounce'] = pronoun.find('ul').text.strip().split()
            summary['explain'] = explain_text(explain)

            grammar = data.select('div#web div.dictionaryWordCard > ul > li')
            summary['grammar'] = list(map(text, grammar))
        except AttributeError as e:
            raise NotFoundError(word)

        # Post-process summary
        if summary.get('pronounce'):
            summary['pronounce'] = list(map(
                lambda x: re.match('(.*)(\[.*\])', x).groups(),
                summary['pronounce']))

        # Handle explain
        content['explain'] = []
        try:
            nodes = data.select('div.tab-content-explanation ul li')

            for node in nodes:
                if re.match('\d', node.text.strip()):
                    s = node.select_one('span')
                    exp = {
                        'type': 'item',
                        'text': s.text,
                    }

                    exp['sentence'] = []
                    for s in node.select('p'):
                        sentence = list(map(
                            lambda x:
                                ('b', x.text) if x.name == 'b' else str(x),
                            s.span.contents))
                        if isinstance(sentence[-1], str):
                            hd, _, tl = sentence.pop().rpartition(' ')
                            sentence.extend([hd, '\n', tl])
                        sentence.append('\n')
                        exp['sentence'].extend(sentence)
                else:
                    exp = {
                        'type': 'PoS',  # part of speech
                        'text': node.text.strip(),
                    }
                content['explain'].append(exp)
        except IndexError:
            raise NotFoundError(word)

        # Extract verbose
        content['verbose'] = []
        synonyms = data.select_one('div.tab-content-synonyms')
        if synonyms:
            content['verbose'].extend(list(map(text, synonyms.select('> *'))))

        record = Record(
            word=word,
            content=json.dumps(content),
            source=self.provider,
        )
        return record
