import json

from pytest import raises
from unittest.mock import Mock, patch

from ...dictionaries.jisho import JishoDict
from ...exceptions import NotFoundError
from ...models import Record


class TestJishoDict:
    def setup_method(self, method):
        self.dict = JishoDict()
        self.content = {
            "data": [
                {
                    "attribution": {
                        "dbpedia": (
                            "http://dbpedia.org/resource/Japanese_language"
                        ),
                        "jmdict": True,
                        "jmnedict": False
                    },
                    "is_common": True,
                    "japanese": [
                        {
                            "reading": "\u306b\u307b\u3093\u3054",
                            "word": "\u65e5\u672c\u8a9e"
                        },
                        {
                            "reading": "\u306b\u3063\u307d\u3093\u3054",
                            "word": "\u65e5\u672c\u8a9e"
                        }
                    ],
                    "senses": [
                        {
                            "antonyms": [],
                            "english_definitions": [
                                "Japanese (language)"
                            ],
                            "info": [],
                            "links": [],
                            "parts_of_speech": [
                                "Noun",
                                "No-adjective"
                            ],
                            "restrictions": [],
                            "see_also": [
                                "\u56fd\u8a9e \u3053\u304f\u3054"
                            ],
                            "source": [],
                            "tags": []
                        },
                        {
                            "antonyms": [],
                            "english_definitions": [
                                "Japanese as a second language"
                            ],
                            "info": [
                                "esp. as a school or university subject"
                            ],
                            "links": [],
                            "parts_of_speech": [
                                "Noun"
                            ],
                            "restrictions": [
                                "\u306b\u307b\u3093\u3054"
                            ],
                            "see_also": [],
                            "source": [],
                            "tags": []
                        },
                        {
                            "antonyms": [],
                            "english_definitions": [
                                "Japanese language"
                            ],
                            "info": [],
                            "links": [
                                {
                                    "text": (
                                        "Read \u201cJapanese language"
                                        "\u201d on English Wikipedia"
                                    ),
                                    "url": (
                                        "http://en.wikipedia.org/wiki/"
                                        "Japanese_language?oldid=495372677"
                                    ),
                                },
                                {
                                    "text": (
                                        "Read \u201c\u65e5\u672c\u8a9e\u201d"
                                        " on Japanese Wikipedia"
                                    ),
                                    "url": (
                                        "http://ja.wikipedia.org/wiki/"
                                        "\u65e5\u672c\u8a9e?oldid=42768780"
                                    ),
                                }
                            ],
                            "parts_of_speech": [
                                "Wikipedia definition"
                            ],
                            "restrictions": [],
                            "see_also": [],
                            "sentences": [],
                            "source": [],
                            "tags": []
                        }
                    ],
                    "tags": [
                        "wanikani10"
                    ]
                },
            ],
            "meta": {
                "status": 200
            }
        }

    def teardown_method(self, method):
        del self.dict

    def test_provider(self):
        assert self.dict.provider == 'jisho'

    def test_title(self):
        assert self.dict.title == 'Jisho'

    def test__get_url(self):
        url = 'http://jisho.org/api/v1/search/words?keyword=辞書'
        assert url == self.dict._get_url('辞書')

    def test_show(self):
        content = json.dumps(self.content)
        print(content)
        r = Record(word='Japanese', content=content, source=self.dict.provider)

        # god bless this method, hope that it do not raise any exception
        self.dict.show(r)

    @patch('zdict.dictionaries.jisho.Record')
    def test_query_normal(self, Record):
        self.content_json = json.dumps(self.content)
        self.dict._get_raw = Mock(return_value=self.content_json)
        self.dict.query('Japanese', timeout=5)
        Record.assert_called_with(
            word='Japanese',
            content=self.content_json,
            source='jisho',
        )

    def test_query_not_found(self):
        self.dict._get_raw = Mock(return_value='{"data": []}')
        with raises(NotFoundError):
            self.dict.query('辞書', timeout=5)
        self.dict._get_raw.assert_called_with('辞書', 5)
