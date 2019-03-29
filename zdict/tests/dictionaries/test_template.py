from pytest import raises
from unittest.mock import Mock, patch

from zdict.exceptions import NotFoundError
from zdict.zdict import get_args

# Change TemplateDict to the class of new dictionary and delete this comment
from zdict.dictionaries.template import TemplateDict


# Change TemplateDict to the class of new dictionary and delete this comment
class TestTemplateDict:
    @classmethod
    def setup_class(cls):
        # Change `Template` to the name of the new dict and delete this comment
        cls.dict = TemplateDict(get_args())
        cls.words = ['style', 'metadata']
        cls.records = [cls.dict.query(word) for word in cls.words]

    @classmethod
    def teardown_class(cls):
        del cls.dict
        del cls.words
        del cls.records

    def test_provider(self):
        # Change `template` to the provider of the new dict and delete this comment
        assert self.dict.provider == 'template'

    def test_title(self):
        # Change `Template Dictionary` to the title of the new dict and delete this comment
        assert self.dict.title == 'Template Dictionary'

    def test__get_url(self):
        # Change url for the new dict and delete this comment
        url = 'https://tw.dictionary.yahoo.com/dictionary?p=test'
        assert url == self.dict._get_url('test')

    def test_show(self):
        # god bless this method, hope that it do not raise any exception
        self.dict.args.verbose = False

        for record in self.records:
            self.dict.show(record)

    def test_show_verbose(self):
        # god bless this method, hope that it do not raise any exception
        self.dict.args.verbose = True

        for record in self.records:
            self.dict.show(record)

    # Change `template` to `{newdict}` for the line below and delete this comment
    @patch('zdict.dictionaries.template.Record')
    def test_query_normal(self, Record):
        self.dict.args.verbose = False

        for i, word in enumerate(self.words):
            self.dict.query(word)
            Record.assert_called_with(
                word=word,
                content=self.records[i].content,
                # Change `template` to the source for the new dictionary and delete this comment
                source='template',
            )

    # Change `template` to `{newdict}` for the line below and delete this comment
    @patch('zdict.dictionaries.template.Record')
    def test_query_verbose(self, Record):
        self.dict.args.verbose = True

        for i, word in enumerate(self.words):
            self.dict.query(word)
            Record.assert_called_with(
                word=word,
                content=self.records[i].content,
                # Change `template` to `{newdict}` for the line below and delete this comment
                source='template',
            )

    def test_query_not_found(self):
        self.dict._get_raw = Mock(return_value='{"data": []}')
        with raises(NotFoundError):
            self.dict.query(self.words[0])
        self.dict._get_raw.assert_called_with(self.words[0])

    # Add other test functions for private functions of the new dictionary class
