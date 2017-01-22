import sys

from contextlib import redirect_stdout
from io import StringIO

from tornado import ioloop, web


class ZdictHandler(web.RequestHandler):
    def initialize(self, executor, zargs):
        self.executor = executor
        self.zargs = zargs

    def get(self, word):
        self.zargs.words = (word,)
        fd = StringIO()

        with redirect_stdout(fd):
            self.executor(self.zargs)

        self.write(fd.getvalue())


def make_app(executor, zargs):
    return web.Application([
        (r"/(\w+)", ZdictHandler, dict(executor=executor, zargs=zargs)),
    ])


def main(executor: 'hack to prevent from recursive import', args):
    app = make_app(executor, args)
    app.listen(8888)
    print("zdict http server started on localhost:8888")
    ioloop.IOLoop.current().start()
