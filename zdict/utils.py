import os
import sys

from zdict import constants


def create_zdict_dir_if_not_exists():
    if not os.path.isdir(constants.BASE_DIR):
        os.mkdir(constants.BASE_DIR)


def create_zdict_db_if_not_exists():
    if not os.path.exists(constants.DB_FILE):
        open(constants.DB_FILE, 'a').close()


def check_zdict_dir_and_db():
    create_zdict_dir_if_not_exists()
    create_zdict_db_if_not_exists()


class ColorConst(type):
    COLOR_TEMPLATE = "\33[{}m"
    COLOR_LIST = (
        ('ORG', 0),
        ('BLACK', 30),
        ('RED', 31),
        ('GREEN', 32),
        ('YELLOW', 33),
        ('BLUE', 34),
        ('MAGENTA', 35),
        ('INDIGO', 36),
        ('WHITE', 37),
    )

    def __getattr__(cls, color):
        '''
        Magic!
        http://stackoverflow.com/questions/3155436
        '''
        d = dict(cls.COLOR_LIST)
        color = color.upper() if color else 'ORG'
        _color = color if color[0] != 'L' else color[1:]

        if _color not in d.keys():
            raise AttributeError

        return cls.COLOR_TEMPLATE.format(
            '{}{}'.format(
                d.get(_color, 0),
                ';1' if color[0] == 'L' else ''
            )
        )


class Color(metaclass=ColorConst):
    _force_color = False

    @classmethod
    def set_force_color(cls, force_color=True):
        cls._force_color = force_color

    @classmethod
    def format(self, s='', color='org', indent=0):
        '''
        :type s: str
        :param s: message
        :param color: predefined color name, e,g,: red, RED.
            Using 'l' prefix for bright color, e.g.: lred, lwhite.
            It's case-insensitive.

            If stdout isn't a tty, the color option will be ignored.
        '''
        colorize = self._force_color or sys.stdout.isatty()

        return '{indent}{color}{s}{org}'.format(
            indent=' ' * indent,
            color=getattr(self, color, '') if colorize else '',
            s=s,
            org=self.ORG if colorize else '',
        )

    @classmethod
    def print(self, *args, end='\n', **kwargs):
        print(self.format(*args, **kwargs), end=end)


def import_readline():
    if sys.platform == 'darwin' and sys.version_info <= (3, 5):
        import gnureadline as readline
    else:
        import readline
    return readline


readline = import_readline()
