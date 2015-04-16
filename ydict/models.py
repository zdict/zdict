import peewee

from .constants import DB_FILE


db = peewee.SqliteDatabase(DB_FILE)


class Record(peewee.Model):
    '''
    A model for storing the query results into the SQLite db.

    :param word: the vocabulary
    :param content: the query result of the vocabulary
    :param source: source of the content. May be Yahoo!, Google, ... Dict

    '''

    word = peewee.TextField()
    content = peewee.TextField()
    source = peewee.CharField()

    class Meta:
        database = db
        primary_key = peewee.CompositeKey('word', 'source')
