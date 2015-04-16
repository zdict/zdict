import os


VERSION = '2.0.0'

BASE_DIR = os.path.join(os.getenv('HOME'), '.ydict')

DB_FILE = os.path.join(BASE_DIR, 'db.sqlite')
