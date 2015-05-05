import abc


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
        Magic! @ http://stackoverflow.com/questions/3155436/getattr-for-static-class-variables-in-python
        '''
        d = dict(cls.COLOR_LIST)
        color = color.upper()
        _color = color if color[0] != 'L' else color[1:]

        if not _color in d.keys():
            raise AttributeError

        return cls.COLOR_TEMPLATE.format(
            '{}{}'.format(
                d.get(_color, 0),
                ';1' if color[0] == 'L' else ''
            )
        )


class Color(metaclass=ColorConst):
    @classmethod
    def format(self, s, color='org', indent=0):
        '''
        :type s: str
        :param s: message
        :param color: predefined color name, e,g,: red, RED.
            Using 'l' prefix for bright color, e.g.: lred, lwhite.
            It's case-insensitive.
        '''
        if s is None:
            return
        return '{indent}{color}{s}{org}'.format(
            indent=' ' * indent,
            color=getattr(self, color, ''),
            s=s,
            org=self.ORG,
        )

    @classmethod
    def print(self, *args, end='\n', **kwargs):
        print(self.format(*args, **kwargs), end=end)


class sequence(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def __item__(self):
        ...


sequence.register(tuple)
sequence.register(list)
sequence.register(type((_ for _ in ())))
