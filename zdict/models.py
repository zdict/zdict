import peewee

from zdict.constants import DB_FILE


db = peewee.SqliteDatabase(DB_FILE)


class Record(peewee.Model):
    '''
    A model for storing the query results into the SQLite db.

    :param word: the vocabulary
    :param content: the query result of the vocabulary.
        It's a json document has the following spec.
        {
            'word': word,
            // storing the querying result.
            'pronounce': [
                ('key', 'value'),
                ...
            ],
            'sound': [
                ('type', 'url'),
                ...
                // type: (mp3|ogg)
            ],
            'explain': [
                ('speech',
                    (
                        'meaning',
                        ('sentence1', 'translation'),
                        ...
                    ),
                    ...
                ),
                ...
            ]
        }
    :param source: source of the content. May be Yahoo!, Google, ... Dict
    '''

    word = peewee.TextField()
    content = peewee.TextField()
    source = peewee.CharField()

    class Meta:
        database = db
        primary_key = peewee.CompositeKey('word', 'source')
