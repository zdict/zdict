class Color:
    def format(self, s, color='org', indent=0):
        '''
        :type s: str
        :param s: message
        :param color: predefined color name, e,g,: red, RED.
            Using 'l' prefix for bright color, e.g.: lred, lwhite.
            It's case-insensitive.
        '''
        COLOR_TEMPLATE = "\33[{}m"
        COLOR_LIST = {
            "ORG": 0,
            "BLACK": 30,
            "RED": 31,
            "GREEN": 32,
            "YELLOW": 33,
            "BLUE": 34,
            "MAGENTA": 35,
            "INDIGO": 36,
            "WHITE": 37,
            }


        def gen_color(name):
            name = name.upper()
            if name[0]=='L':
                return COLOR_TEMPLATE.format('{};1'.format(COLOR_LIST[name[1:]]))
            else:
                return COLOR_TEMPLATE.format(COLOR_LIST[name])

        return '{indent}{color}{s}{org}'.format(
            indent=' ' * indent,
            color=gen_color(color),
            s=s,
            org=gen_color("ORG"),
        )

    @classmethod
    def print(self, *args, end='\n', **kwargs):
        return print(self.format(*args, **kwargs), end=end)
