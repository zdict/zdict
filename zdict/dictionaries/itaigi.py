import json

import requests
from bs4 import BeautifulSoup

from zdict.dictionary import DictBase
from zdict.exceptions import NotFoundError
from zdict.models import Record


class iTaigiDict(DictBase):

    API = 'https://itaigi.tw/平臺項目列表/揣列表?關鍵字={word}'

    @property
    def provider(self):
        return 'itaigi'

    @property
    def title(self):
        return 'iTaigi - 愛台語'

    def _get_url(self, word) -> str:
        return self.API.format(word=word)

    def _get_word_text(self, word) -> str:
        try:
            text = word["文本資料"]
        except AttributeError:
            raise
        return text

    def _get_word_pronounce(self, word) -> str:
        try:
            pronounce = word["音標資料"]
        except AttributeError:
            raise
        return pronounce

    def _get_word_sentences(self, text, pronounce) -> dict:
        API = "https://xn--fsqx9h.xn--v0qr21b.xn--kpry57d/%E7%9C%8B/?%E6%BC%A2%E5%AD%97={text}&%E8%87%BA%E7%BE%85={pronounce}"
        url = API.format(text=text, pronounce=pronounce)

        try:
            _ = json.loads(requests.get(url).text)
        except Exception:
            return {}

        '''
        try:
            chinese_sentence = _["例句"][0]["漢字"]
        except Exception:
            raise

        d = {
            'mandarin': mandarin_sentence,
            'chinese': chinese_sentence,
            'taiwanese': taiwanese_sentence,
        }
        '''
        return {}

    def query(self, word: str):
        webpage = self._get_raw(word)
        soup = BeautifulSoup(webpage, "html.parser")
        response = json.loads(soup.text)
        content = {}

        # Not Found
        if not response["列表"]:
            raise NotFoundError(word)

        # Show Chinese word from iTaigi in stead of user input if possible
        try:
            word = response["列表"][0]["外語資料"]
        except Exception:
            pass

        # Fetch basic words with text, pronounce and sentence
        try:
            basic_words = response["列表"][0]["新詞文本"]
        except Exception:
            raise

        content['basic_words'] = []
        for basic_word in basic_words:
            d = {}

            text = self._get_word_text(basic_word)
            d['text'] = text

            pronounce = self._get_word_pronounce(basic_word)
            d['pronounce'] = pronounce

            if self.args.verbose:
                sentences = self._get_word_sentences(text, pronounce)
                d['sentences'] = sentences

            content['basic_words'].append(d)

        if response["其他建議"]:
            try:
                related_words = response["其他建議"]
            except Exception:
                raise

            content['related_words'] = []
            for related_word in related_words:
                d = {}

                text = self._get_word_text(related_word)
                d['text'] = text

                pronounce = self._get_word_pronounce(related_word)
                d['pronounce'] = pronounce

                if self.args.verbose:
                    sentences = self._get_word_sentences(text, pronounce)
                    d['sentences'] = sentences

                content['related_words'].append(d)

        record = Record(
            word=word,
            content=json.dumps(content),
            source=self.provider,
        )

        return record

    def show(self, record: Record):
        content = json.loads(record.content)

        # from pprint import pprint
        # pprint(content, indent=4)

        self.color.print(record.word, 'yellow')

        # print basic_words
        for basic_word in content['basic_words']:
            self.color.print(basic_word['text'], end=' ', indent=2)
            self.color.print(basic_word['pronounce'], 'lwhite')

            if self.args.verbose:
                # TODO: print sentences
                pass

        if content['related_words']:
            print()
            self.color.print("相關字詞", 'lred', indent=2)
            # print related_words
            for related_word in content['related_words']:
                self.color.print(related_word['text'], end=' ', indent=4)
                self.color.print(related_word['pronounce'], 'lwhite')

                if self.args.verbose:
                    # TODO: print sentences
                    pass
