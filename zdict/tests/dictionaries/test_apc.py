from pytest import raises
from unittest.mock import patch

from zdict.exceptions import NotFoundError
from zdict.zdict import get_args

from zdict.dictionaries.apc import ApcDict


class TestApcDict:
    @classmethod
    def setup_class(cls):
        cls.dict = ApcDict(get_args())

        # You may want to change words to some certain test cases.
        cls.words = ["utux", "tux"]
        cls.not_found_word = "dsafwwe"

        # Setup normal query data
        cls.dict.args.verbose = False
        cls.records = [cls.dict.query(word) for word in cls.words]

        # Setup verbose query data
        cls.dict.args.verbose = True
        cls.verbose_records = [cls.dict.query(word) for word in cls.words]

        # Change back to default verbose config
        cls.dict.args.verbose = False

    @classmethod
    def teardown_class(cls):
        del cls.dict
        del cls.words
        del cls.not_found_word
        del cls.records
        del cls.verbose_records

    def test_provider(self):
        assert self.dict.provider == "apc"

    def test_title(self):
        assert self.dict.title == "原住民族委員會 - 原住民族語言線上詞典"

    def test__get_url(self):
        url = "https://e-dictionary.apc.gov.tw/search/list.htm"
        assert url == self.dict._get_url("test")

    def test_show(self):
        self.dict.args.verbose = False

        for record in self.records:
            self.dict.show(record)

    def test_show_verbose(self):
        self.dict.args.verbose = True

        for record in self.verbose_records:
            self.dict.show(record)

    @patch("zdict.dictionaries.apc.Record")
    def test_query_normal(self, Record):
        self.dict.args.verbose = False

        for i, word in enumerate(self.words):
            self.dict.query(word)
            Record.assert_called_with(
                word=word, content=self.records[i].content, source="apc",
            )

    @patch("zdict.dictionaries.apc.Record")
    def test_query_verbose(self, Record):
        self.dict.args.verbose = True

        for i, word in enumerate(self.words):
            self.dict.query(word)
            Record.assert_called_with(
                word=word,
                content=self.verbose_records[i].content,
                source="apc",
            )

    def test_query_not_found(self):
        # Trigger NotFoundError intentionally and see if it works.
        with raises(NotFoundError):
            self.dict.query(self.not_found_word)
