import os


VERSION = '2.0.0'

BASE_DIR_NAME = '.ydict'
BASE_DIR = os.path.join(os.getenv('HOME'), BASE_DIR_NAME)

DB_NAME = 'sqlite.db'
DB_FILE = os.path.join(BASE_DIR, DB_NAME)
