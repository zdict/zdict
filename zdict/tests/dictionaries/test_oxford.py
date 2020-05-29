# flake8: noqa
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
        uri = 'https://od-api.oxforddictionaries.com/api/v2/entries/en/mock'
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
    "id": "string",
    "metadata": {
        "operation": "retrieve",
        "provider": "Oxford University Press",
        "schema": "RetrieveEntry"
    },
    "results": [
        {
            "id": "string",
            "language": "en-gb",
            "lexicalEntries": [
                {
                    "derivatives": [
                        {
                            "id": "stringless",
                            "text": "stringless"
                        },
                        {
                            "id": "stringlike",
                            "text": "stringlike"
                        }
                    ],
                    "entries": [
                        {
                            "etymologies": [
                                "Old English streng (noun), of Germanic origin; related to German Strang, also to strong. The verb (dating from late Middle English) is first recorded in the senses ‘arrange in a row’ and ‘fit with a string’"
                            ],
                            "pronunciations": [
                                {
                                    "audioFile": "https://audio.oxforddictionaries.com/en/mp3/string_gb_1.mp3",
                                    "dialects": [
                                        "British English"
                                    ],
                                    "phoneticNotation": "IPA",
                                    "phoneticSpelling": "strɪŋ"
                                }
                            ],
                            "senses": [
                                {
                                    "definitions": [
                                        "material consisting of threads of cotton, hemp, or other material twisted together to form a thin length"
                                    ],
                                    "examples": [
                                        {
                                            "text": "unwieldy packs tied up with string"
                                        }
                                    ],
                                    "id": "m_en_gbus1003050.006",
                                    "notes": [
                                        {
                                            "text": "mass noun",
                                            "type": "grammaticalNote"
                                        }
                                    ],
                                    "shortDefinitions": [
                                        "material consisting of threads of cotton, hemp"
                                    ],
                                    "subsenses": [
                                        {
                                            "definitions": [
                                                "a piece of string used to tie round or attach to something"
                                            ],
                                            "examples": [
                                                {
                                                    "text": "the elephant mask had a trunk you could raise by pulling a string"
                                                }
                                            ],
                                            "id": "m_en_gbus1003050.008",
                                            "notes": [
                                                {
                                                    "text": "count noun",
                                                    "type": "grammaticalNote"
                                                }
                                            ],
                                            "shortDefinitions": [
                                                "piece of string used to tie round or attach to something"
                                            ]
                                        },
                                        {
                                            "definitions": [
                                                "a piece of catgut or similar material interwoven with others to form the head of a sports racket."
                                            ],
                                            "domains": [
                                                {
                                                    "id": "sport",
                                                    "text": "Sport"
                                                }
                                            ],
                                            "id": "m_en_gbus1003050.011",
                                            "notes": [
                                                {
                                                    "text": "count noun",
                                                    "type": "grammaticalNote"
                                                }
                                            ],
                                            "shortDefinitions": [
                                                "piece of catgut or similar material interwoven with others"
                                            ]
                                        },
                                        {
                                            "definitions": [
                                                "a length of catgut or wire on a musical instrument, producing a note by vibration"
                                            ],
                                            "domains": [
                                                {
                                                    "id": "music",
                                                    "text": "Music"
                                                }
                                            ],
                                            "examples": [
                                                {
                                                    "text": "the D string broke"
                                                }
                                            ],
                                            "id": "m_en_gbus1003050.012",
                                            "notes": [
                                                {
                                                    "text": "count noun",
                                                    "type": "grammaticalNote"
                                                }
                                            ],
                                            "shortDefinitions": [
                                                "length of catgut or wire on musical instrument"
                                            ]
                                        },
                                        {
                                            "definitions": [
                                                "the stringed instruments in an orchestra"
                                            ],
                                            "domains": [
                                                {
                                                    "id": "instrument",
                                                    "text": "Instrument"
                                                }
                                            ],
                                            "examples": [
                                                {
                                                    "text": "the blend of the wind-group is less perfect than that of the strings"
                                                }
                                            ],
                                            "id": "m_en_gbus1003050.013",
                                            "notes": [
                                                {
                                                    "text": "strings",
                                                    "type": "wordFormNote"
                                                }
                                            ],
                                            "shortDefinitions": [
                                                "stringed instruments in orchestra"
                                            ],
                                            "synonyms": [
                                                {
                                                    "language": "en",
                                                    "text": "stringed instruments"
                                                }
                                            ],
                                            "thesaurusLinks": [
                                                {
                                                    "entry_id": "string",
                                                    "sense_id": "t_en_gb0014229.006"
                                                }
                                            ]
                                        },
                                        {
                                            "definitions": [
                                                "relating to or consisting of stringed instruments"
                                            ],
                                            "examples": [
                                                {
                                                    "text": "a string quartet"
                                                }
                                            ],
                                            "id": "m_en_gbus1003050.015",
                                            "notes": [
                                                {
                                                    "text": "as modifier",
                                                    "type": "grammaticalNote"
                                                }
                                            ],
                                            "shortDefinitions": [
                                                "relating to or consisting of stringed instruments"
                                            ]
                                        }
                                    ],
                                    "synonyms": [
                                        {
                                            "language": "en",
                                            "text": "twine"
                                        },
                                        {
                                            "language": "en",
                                            "text": "cord"
                                        },
                                        {
                                            "language": "en",
                                            "text": "yarn"
                                        },
                                        {
                                            "language": "en",
                                            "text": "thread"
                                        },
                                        {
                                            "language": "en",
                                            "text": "strand"
                                        },
                                        {
                                            "language": "en",
                                            "text": "fibre"
                                        }
                                    ],
                                    "thesaurusLinks": [
                                        {
                                            "entry_id": "string",
                                            "sense_id": "t_en_gb0014229.001"
                                        }
                                    ]
                                },
                                {
                                    "constructions": [
                                        {
                                            "text": "a string of"
                                        }
                                    ],
                                    "definitions": [
                                        "a set of things tied or threaded together on a thin cord"
                                    ],
                                    "examples": [
                                        {
                                            "text": "she wore a string of agates round her throat"
                                        }
                                    ],
                                    "id": "m_en_gbus1003050.018",
                                    "shortDefinitions": [
                                        "set of things tied or threaded together on thin cord"
                                    ],
                                    "subsenses": [
                                        {
                                            "constructions": [
                                                {
                                                    "text": "a string of"
                                                }
                                            ],
                                            "definitions": [
                                                "a sequence of similar items or events"
                                            ],
                                            "examples": [
                                                {
                                                    "text": "a string of burglaries"
                                                }
                                            ],
                                            "id": "m_en_gbus1003050.019",
                                            "shortDefinitions": [
                                                "sequence of similar items or events"
                                            ],
                                            "synonyms": [
                                                {
                                                    "language": "en",
                                                    "text": "series"
                                                },
                                                {
                                                    "language": "en",
                                                    "text": "succession"
                                                },
                                                {
                                                    "language": "en",
                                                    "text": "chain"
                                                },
                                                {
                                                    "language": "en",
                                                    "text": "sequence"
                                                },
                                                {
                                                    "language": "en",
                                                    "text": "concatenation"
                                                },
                                                {
                                                    "language": "en",
                                                    "text": "run"
                                                },
                                                {
                                                    "language": "en",
                                                    "text": "streak"
                                                }
                                            ],
                                            "thesaurusLinks": [
                                                {
                                                    "entry_id": "string",
                                                    "sense_id": "t_en_gb0014229.003"
                                                }
                                            ]
                                        },
                                        {
                                            "definitions": [
                                                "a linear sequence of characters, words, or other data."
                                            ],
                                            "domains": [
                                                {
                                                    "id": "computing",
                                                    "text": "Computing"
                                                }
                                            ],
                                            "id": "m_en_gbus1003050.020",
                                            "shortDefinitions": [
                                                "linear sequence of data"
                                            ]
                                        },
                                        {
                                            "definitions": [
                                                "a group of racehorses trained at one stable."
                                            ],
                                            "domains": [
                                                {
                                                    "id": "racing",
                                                    "text": "Racing"
                                                }
                                            ],
                                            "id": "m_en_gbus1003050.021",
                                            "shortDefinitions": [
                                                "group of racehorses trained at one stable"
                                            ]
                                        },
                                        {
                                            "definitions": [
                                                "a reserve team or player holding a specified position in an order of preference"
                                            ],
                                            "domains": [
                                                {
                                                    "id": "sport",
                                                    "text": "Sport"
                                                }
                                            ],
                                            "examples": [
                                                {
                                                    "text": "the village team held Rangers' second string to a 0–0 draw"
                                                }
                                            ],
                                            "id": "m_en_gbus1003050.022",
                                            "shortDefinitions": [
                                                "reserve team or player holding specified position in order of preference"
                                            ]
                                        },
                                        {
                                            "definitions": [
                                                "a player assigned a specified rank in a team in an individual sport such as squash"
                                            ],
                                            "domains": [
                                                {
                                                    "id": "sport",
                                                    "text": "Sport"
                                                }
                                            ],
                                            "examples": [
                                                {
                                                    "text": "Taylor lost to third string Baines"
                                                }
                                            ],
                                            "id": "m_en_gbus1003050.023",
                                            "shortDefinitions": [
                                                "player assigned specified rank in team in individual sport such as squash"
                                            ]
                                        }
                                    ],
                                    "synonyms": [
                                        {
                                            "language": "en",
                                            "text": "strand"
                                        },
                                        {
                                            "language": "en",
                                            "text": "rope"
                                        },
                                        {
                                            "language": "en",
                                            "text": "necklace"
                                        },
                                        {
                                            "language": "en",
                                            "text": "rosary"
                                        },
                                        {
                                            "language": "en",
                                            "text": "chaplet"
                                        }
                                    ],
                                    "thesaurusLinks": [
                                        {
                                            "entry_id": "string",
                                            "sense_id": "t_en_gb0014229.005"
                                        }
                                    ]
                                },
                                {
                                    "definitions": [
                                        "a tough piece of fibre in vegetables, meat, or other food, such as a tough elongated piece connecting the two halves of a bean pod."
                                    ],
                                    "domains": [
                                        {
                                            "id": "food",
                                            "text": "Food"
                                        }
                                    ],
                                    "id": "m_en_gbus1003050.025",
                                    "shortDefinitions": [
                                        "tough piece of fibre in food"
                                    ]
                                },
                                {
                                    "definitions": [
                                        "a G-string or thong."
                                    ],
                                    "domains": [
                                        {
                                            "id": "clothing",
                                            "text": "Clothing"
                                        }
                                    ],
                                    "id": "m_en_gbus1003050.027",
                                    "shortDefinitions": [
                                        "G-string or thong"
                                    ]
                                },
                                {
                                    "crossReferenceMarkers": [
                                        "short for stringboard"
                                    ],
                                    "crossReferences": [
                                        {
                                            "id": "stringboard",
                                            "text": "stringboard",
                                            "type": "abbreviation of"
                                        }
                                    ],
                                    "id": "m_en_gbus1003050.029"
                                },
                                {
                                    "definitions": [
                                        "a hypothetical one-dimensional subatomic particle having the dynamical properties of a flexible loop."
                                    ],
                                    "domains": [
                                        {
                                            "id": "physics",
                                            "text": "Physics"
                                        }
                                    ],
                                    "id": "m_en_gbus1003050.031",
                                    "shortDefinitions": [
                                        "hypothetical one-dimensional subatomic particle having dynamical properties of flexible loop"
                                    ],
                                    "subsenses": [
                                        {
                                            "definitions": [
                                                "a hypothetical threadlike concentration of energy within the structure of space–time."
                                            ],
                                            "domains": [
                                                {
                                                    "id": "physics",
                                                    "text": "Physics"
                                                }
                                            ],
                                            "id": "m_en_gbus1003050.032",
                                            "shortDefinitions": [
                                                "hypothetical thread-like concentration of energy within structure of space-time"
                                            ],
                                            "variantForms": [
                                                {
                                                    "text": "cosmic string"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "language": "en-gb",
                    "lexicalCategory": {
                        "id": "noun",
                        "text": "Noun"
                    },
                    "phrasalVerbs": [
                        {
                            "id": "string_along",
                            "text": "string along"
                        },
                        {
                            "id": "string_out",
                            "text": "string out"
                        },
                        {
                            "id": "string_together",
                            "text": "string together"
                        },
                        {
                            "id": "string_up",
                            "text": "string up"
                        }
                    ],
                    "phrases": [
                        {
                            "id": "how_long_is_a_piece_of_string%3F",
                            "text": "how long is a piece of string?"
                        },
                        {
                            "id": "no_strings_attached",
                            "text": "no strings attached"
                        },
                        {
                            "id": "on_a_string",
                            "text": "on a string"
                        }
                    ],
                    "text": "string"
                },
                {
                    "derivatives": [
                        {
                            "id": "stringless",
                            "text": "stringless"
                        },
                        {
                            "id": "stringlike",
                            "text": "stringlike"
                        }
                    ],
                    "entries": [
                        {
                            "inflections": [
                                {
                                    "grammaticalFeatures": [
                                        {
                                            "id": "pastParticiple",
                                            "text": "Past Participle",
                                            "type": "Non Finiteness"
                                        },
                                        {
                                            "id": "past",
                                            "text": "Past",
                                            "type": "Tense"
                                        }
                                    ],
                                    "inflectedForm": "strung",
                                    "pronunciations": [
                                        {
                                            "audioFile": "https://audio.oxforddictionaries.com/en/mp3/strung_gb_1.mp3",
                                            "dialects": [
                                                "British English"
                                            ],
                                            "phoneticNotation": "IPA",
                                            "phoneticSpelling": "strʌŋ"
                                        }
                                    ]
                                }
                            ],
                            "pronunciations": [
                                {
                                    "audioFile": "https://audio.oxforddictionaries.com/en/mp3/string_gb_1.mp3",
                                    "dialects": [
                                        "British English"
                                    ],
                                    "phoneticNotation": "IPA",
                                    "phoneticSpelling": "strɪŋ"
                                }
                            ],
                            "senses": [
                                {
                                    "definitions": [
                                        "hang (something) so that it stretches in a long line"
                                    ],
                                    "examples": [
                                        {
                                            "text": "lights were strung across the promenade"
                                        }
                                    ],
                                    "id": "m_en_gbus1003050.041",
                                    "notes": [
                                        {
                                            "text": "with object and adverbial",
                                            "type": "grammaticalNote"
                                        }
                                    ],
                                    "shortDefinitions": [
                                        "hang something so that it stretches in long line"
                                    ],
                                    "subsenses": [
                                        {
                                            "definitions": [
                                                "thread (a series of small objects) on a string"
                                            ],
                                            "examples": [
                                                {
                                                    "text": "he collected stones with holes in them and strung them on a strong cord"
                                                }
                                            ],
                                            "id": "m_en_gbus1003050.047",
                                            "shortDefinitions": [
                                                "thread series of small objects on string"
                                            ],
                                            "synonyms": [
                                                {
                                                    "language": "en",
                                                    "text": "thread"
                                                },
                                                {
                                                    "language": "en",
                                                    "text": "loop"
                                                },
                                                {
                                                    "language": "en",
                                                    "text": "link"
                                                },
                                                {
                                                    "language": "en",
                                                    "text": "join"
                                                }
                                            ],
                                            "thesaurusLinks": [
                                                {
                                                    "entry_id": "string",
                                                    "sense_id": "t_en_gb0014229.010"
                                                }
                                            ]
                                        },
                                        {
                                            "definitions": [
                                                "be arranged in a long line"
                                            ],
                                            "examples": [
                                                {
                                                    "text": "the houses were strung along the road"
                                                }
                                            ],
                                            "id": "m_en_gbus1003050.048",
                                            "notes": [
                                                {
                                                    "text": "be strung",
                                                    "type": "wordFormNote"
                                                }
                                            ],
                                            "shortDefinitions": [
                                                "be arranged in long line"
                                            ],
                                            "synonyms": [
                                                {
                                                    "language": "en",
                                                    "text": "spread out"
                                                },
                                                {
                                                    "language": "en",
                                                    "text": "space out"
                                                },
                                                {
                                                    "language": "en",
                                                    "text": "set apart"
                                                },
                                                {
                                                    "language": "en",
                                                    "text": "place at intervals"
                                                },
                                                {
                                                    "language": "en",
                                                    "text": "distribute"
                                                },
                                                {
                                                    "language": "en",
                                                    "text": "extend"
                                                },
                                                {
                                                    "language": "en",
                                                    "text": "fan out"
                                                },
                                                {
                                                    "language": "en",
                                                    "text": "scatter"
                                                },
                                                {
                                                    "language": "en",
                                                    "text": "straggle"
                                                }
                                            ],
                                            "thesaurusLinks": [
                                                {
                                                    "entry_id": "string_something_out",
                                                    "sense_id": "t_en_gb0014229.014"
                                                }
                                            ]
                                        }
                                    ],
                                    "synonyms": [
                                        {
                                            "language": "en",
                                            "text": "hang"
                                        },
                                        {
                                            "language": "en",
                                            "text": "suspend"
                                        },
                                        {
                                            "language": "en",
                                            "text": "sling"
                                        },
                                        {
                                            "language": "en",
                                            "text": "stretch"
                                        },
                                        {
                                            "language": "en",
                                            "text": "stretch"
                                        },
                                        {
                                            "language": "en",
                                            "text": "sling"
                                        },
                                        {
                                            "language": "en",
                                            "text": "run"
                                        },
                                        {
                                            "language": "en",
                                            "text": "fasten"
                                        },
                                        {
                                            "language": "en",
                                            "text": "tie"
                                        },
                                        {
                                            "language": "en",
                                            "text": "secure"
                                        },
                                        {
                                            "language": "en",
                                            "text": "link"
                                        }
                                    ],
                                    "thesaurusLinks": [
                                        {
                                            "entry_id": "string",
                                            "sense_id": "t_en_gb0014229.008"
                                        },
                                        {
                                            "entry_id": "string",
                                            "sense_id": "t_en_gb0014229.009"
                                        }
                                    ]
                                },
                                {
                                    "definitions": [
                                        "fit a string or strings to (a musical instrument, a racket, or a bow)"
                                    ],
                                    "examples": [
                                        {
                                            "text": "the harp had been newly strung"
                                        }
                                    ],
                                    "id": "m_en_gbus1003050.052",
                                    "notes": [
                                        {
                                            "text": "with object",
                                            "type": "grammaticalNote"
                                        }
                                    ],
                                    "shortDefinitions": [
                                        "fit string or strings to"
                                    ]
                                },
                                {
                                    "definitions": [
                                        "remove the strings from (a bean)."
                                    ],
                                    "id": "m_en_gbus1003050.054",
                                    "notes": [
                                        {
                                            "text": "with object",
                                            "type": "grammaticalNote"
                                        }
                                    ],
                                    "shortDefinitions": [
                                        "remove strings from"
                                    ]
                                },
                                {
                                    "definitions": [
                                        "hoax or trick (someone)"
                                    ],
                                    "domains": [
                                        {
                                            "id": "billiards",
                                            "text": "Billiards"
                                        }
                                    ],
                                    "examples": [
                                        {
                                            "text": "I'm not stringing you—I'll eat my shirt if it's not true"
                                        }
                                    ],
                                    "id": "m_en_gbus1003050.056",
                                    "notes": [
                                        {
                                            "text": "with object",
                                            "type": "grammaticalNote"
                                        }
                                    ],
                                    "regions": [
                                        {
                                            "id": "north_american",
                                            "text": "North_American"
                                        }
                                    ],
                                    "registers": [
                                        {
                                            "id": "informal",
                                            "text": "Informal"
                                        }
                                    ],
                                    "shortDefinitions": [
                                        "hoax or trick"
                                    ]
                                },
                                {
                                    "definitions": [
                                        "work as a stringer in journalism"
                                    ],
                                    "domains": [
                                        {
                                            "id": "journalism",
                                            "text": "Journalism"
                                        }
                                    ],
                                    "examples": [
                                        {
                                            "text": "he strings for almost every French radio service"
                                        }
                                    ],
                                    "id": "m_en_gbus1003050.058",
                                    "notes": [
                                        {
                                            "text": "no object",
                                            "type": "grammaticalNote"
                                        }
                                    ],
                                    "registers": [
                                        {
                                            "id": "informal",
                                            "text": "Informal"
                                        }
                                    ],
                                    "shortDefinitions": [
                                        "work as stringer in journalism"
                                    ]
                                },
                                {
                                    "definitions": [
                                        "determine the order of play by striking the cue ball from baulk to rebound off the top cushion, first stroke going to the player whose ball comes to rest nearer the bottom cushion."
                                    ],
                                    "domains": [
                                        {
                                            "id": "billiards",
                                            "text": "Billiards"
                                        }
                                    ],
                                    "id": "m_en_gbus1003050.060",
                                    "notes": [
                                        {
                                            "text": "no object",
                                            "type": "grammaticalNote"
                                        }
                                    ],
                                    "shortDefinitions": [
                                        "determine order of play by striking cue ball from baulk to rebound off top cushion"
                                    ]
                                }
                            ]
                        }
                    ],
                    "language": "en-gb",
                    "lexicalCategory": {
                        "id": "verb",
                        "text": "Verb"
                    },
                    "phrasalVerbs": [
                        {
                            "id": "string_along",
                            "text": "string along"
                        },
                        {
                            "id": "string_out",
                            "text": "string out"
                        },
                        {
                            "id": "string_together",
                            "text": "string together"
                        },
                        {
                            "id": "string_up",
                            "text": "string up"
                        }
                    ],
                    "phrases": [
                        {
                            "id": "how_long_is_a_piece_of_string%3F",
                            "text": "how long is a piece of string?"
                        },
                        {
                            "id": "no_strings_attached",
                            "text": "no strings attached"
                        },
                        {
                            "id": "on_a_string",
                            "text": "on a string"
                        }
                    ],
                    "text": "string"
                }
            ],
            "type": "headword",
            "word": "string"
        }
    ],
    "word": "string"
}
"""
