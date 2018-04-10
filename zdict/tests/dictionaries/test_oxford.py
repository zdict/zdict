from pytest import raises
from unittest.mock import Mock, mock_open, patch

from zdict.dictionaries.oxford import OxfordDictionary
from zdict.exceptions import NotFoundError, QueryError
from zdict.models import Record
from zdict.zdict import get_args


class TestOxfordDictionary:
    def setup_method(self, method):
        self.dict = OxfordDictionary(get_args())

    def teardown_method(self, method):
        del self.dict

    def test_provider(self):
        assert self.dict.provider == 'oxford'

    def test__get_url(self):
        uri = 'https://od-api.oxforddictionaries.com/api/v1/entries/en/mock'
        assert self.dict._get_url('mock') == uri

    @patch('os.path.exists')
    def test__get_app_key(self, exists):
        key_file = mock_open(read_data="""
            test_app_id,
            test_app_key """)

        with patch('builtins.open', key_file):
            app_id, app_key = self.dict._get_app_key()

        assert app_id == 'test_app_id'
        assert app_key == 'test_app_key'

    def test_query_notfound(self):
        self.dict._get_raw = Mock(side_effect=QueryError('mock', 404))
        self.dict._get_app_key = Mock(return_value=('id', 'key'))

        with raises(NotFoundError):
            self.dict.query('mock')

        self.dict._get_raw.assert_called_with('mock', headers={
            'app_id': 'id',
            'app_key': 'key'
        })

    @patch('zdict.dictionaries.oxford.Record')
    def test_query_normal(self, Record):
        self.dict._get_raw = Mock(return_value=SAMPLE_RESPONSE)
        self.dict._get_app_key = Mock(return_value=('id', 'key'))

        self.dict.query('string')

        Record.assert_called_with(word='string',
                                  content=SAMPLE_RESPONSE,
                                  source='oxford')

    def test_show(self):
        r = Record(word='string',
                   content=SAMPLE_RESPONSE,
                   source=self.dict.provider)
        self.dict.show(r)


# the sample response copied from the official website
SAMPLE_RESPONSE = """
{
  "metadata": {},
  "results": [
    {
      "id": "string",
      "language": "string",
      "lexicalEntries": [
        {
          "derivativeOf": [
            {
              "domains": [
                "string"
              ],
              "id": "string",
              "language": "string",
              "regions": [
                "string"
              ],
              "registers": [
                "string"
              ],
              "text": "string"
            }
          ],
          "derivatives": [
            {
              "domains": [
                "string"
              ],
              "id": "string",
              "language": "string",
              "regions": [
                "string"
              ],
              "registers": [
                "string"
              ],
              "text": "string"
            }
          ],
          "entries": [
            {
              "etymologies": [
                "string"
              ],
              "grammaticalFeatures": [
                {
                  "text": "string",
                  "type": "string"
                }
              ],
              "homographNumber": "string",
              "notes": [
                {
                  "id": "string",
                  "text": "string",
                  "type": "string"
                }
              ],
              "pronunciations": [
                {
                  "audioFile": "string",
                  "dialects": [
                    "string"
                  ],
                  "phoneticNotation": "string",
                  "phoneticSpelling": "string",
                  "regions": [
                    "string"
                  ]
                }
              ],
              "senses": [
                {
                  "crossReferenceMarkers": [
                    "string"
                  ],
                  "crossReferences": [
                    {
                      "id": "string",
                      "text": "string",
                      "type": "string"
                    }
                  ],
                  "definitions": [
                    "string"
                  ],
                  "domains": [
                    "string"
                  ],
                  "examples": [
                    {
                      "definitions": [
                        "string"
                      ],
                      "domains": [
                        "string"
                      ],
                      "notes": [
                        {
                          "id": "string",
                          "text": "string",
                          "type": "string"
                        }
                      ],
                      "regions": [
                        "string"
                      ],
                      "registers": [
                        "string"
                      ],
                      "senseIds": [
                        "string"
                      ],
                      "text": "string",
                      "translations": [
                        {
                          "domains": [
                            "string"
                          ],
                          "grammaticalFeatures": [
                            {
                              "text": "string",
                              "type": "string"
                            }
                          ],
                          "language": "string",
                          "notes": [
                            {
                              "id": "string",
                              "text": "string",
                              "type": "string"
                            }
                          ],
                          "regions": [
                            "string"
                          ],
                          "registers": [
                            "string"
                          ],
                          "text": "string"
                        }
                      ]
                    }
                  ],
                  "id": "string",
                  "notes": [
                    {
                      "id": "string",
                      "text": "string",
                      "type": "string"
                    }
                  ],
                  "pronunciations": [
                    {
                      "audioFile": "string",
                      "dialects": [
                        "string"
                      ],
                      "phoneticNotation": "string",
                      "phoneticSpelling": "string",
                      "regions": [
                        "string"
                      ]
                    }
                  ],
                  "regions": [
                    "string"
                  ],
                  "registers": [
                    "string"
                  ],
                  "short_definitions": [
                    "string"
                  ],
                  "subsenses": [
                    {}
                  ],
                  "thesaurusLinks": [
                    {
                      "entry_id": "string",
                      "sense_id": "string"
                    }
                  ],
                  "translations": [
                    {
                      "domains": [
                        "string"
                      ],
                      "grammaticalFeatures": [
                        {
                          "text": "string",
                          "type": "string"
                        }
                      ],
                      "language": "string",
                      "notes": [
                        {
                          "id": "string",
                          "text": "string",
                          "type": "string"
                        }
                      ],
                      "regions": [
                        "string"
                      ],
                      "registers": [
                        "string"
                      ],
                      "text": "string"
                    }
                  ],
                  "variantForms": [
                    {
                      "regions": [
                        "string"
                      ],
                      "text": "string"
                    }
                  ]
                }
              ],
              "variantForms": [
                {
                  "regions": [
                    "string"
                  ],
                  "text": "string"
                }
              ]
            }
          ],
          "grammaticalFeatures": [
            {
              "text": "string",
              "type": "string"
            }
          ],
          "language": "string",
          "lexicalCategory": "string",
          "notes": [
            {
              "id": "string",
              "text": "string",
              "type": "string"
            }
          ],
          "pronunciations": [
            {
              "audioFile": "string",
              "dialects": [
                "string"
              ],
              "phoneticNotation": "string",
              "phoneticSpelling": "string",
              "regions": [
                "string"
              ]
            }
          ],
          "text": "string",
          "variantForms": [
            {
              "regions": [
                "string"
              ],
              "text": "string"
            }
          ]
        }
      ],
      "pronunciations": [
        {
          "audioFile": "string",
          "dialects": [
            "string"
          ],
          "phoneticNotation": "string",
          "phoneticSpelling": "string",
          "regions": [
            "string"
          ]
        }
      ],
      "type": "string",
      "word": "string"
    }
  ]
}
"""
