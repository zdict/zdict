'''
The zdict config module

This module create a conf daemon thread for us via ``start_conf_thread``.
The thread hold all the configs. We just access it via ``conf`` object
simply.

Usage:

>>> from zdict.conf import conf, start_conf_thread
>>> start_conf_thread()
>>> conf.foo
'bar'
>>> conf.truth = 42
'''

import logging

from copy import deepcopy
from queue import Queue
from threading import Event, Thread


__all__ = (
    'start_conf_thread',
    'conf',
)

logger = logging.getLogger(__name__)


class _ConfWorker:
    mq = Queue()

    @classmethod
    def conf_thread(cls):
        '''
        The config IO deamon thread
        '''
        conf = cls.load_ini()
        conf.update(cls.load_py())

        while True:
            msg = cls.mq.get(block=True)

            logger.debug(msg)

            if msg.method == 'get':
                # msg.value is a _Future object
                if msg.name not in conf:
                    msg.value.set_error()
                    continue
                msg.value.set(deepcopy(conf[msg.name]))
            elif msg.method == 'set':
                conf[msg.name] = msg.value

    @classmethod
    def start_thread(cls):
        '''
        :return: the ``threading.Thread`` object
        '''
        if hasattr(cls, '_conf_thread') and cls._conf_thread.is_alive():
            raise RuntimeError('Config thread already started')

        cls._conf_thread = Thread(target=cls.conf_thread, daemon=True)
        cls._conf_thread.start()

        return cls._conf_thread

    @classmethod
    def get(cls, name):
        msg = _Message('get', name)
        cls.mq.put(msg)

        ret = msg.value.result  # msg.value is a _Future object
        if msg.value.error:
            raise AttributeError(msg.name)
        return ret

    @classmethod
    def set(cls, name, value):
        msg = _Message('set', name, value)
        cls.mq.put(msg)

    @staticmethod
    def load_ini():
        '''
        Load from ``CONF_INI`` (``BASE_DIR/config.ini``)

        :return: dict
        '''
        logger.warn('method "load_ini" not implemented, return dummy')
        return {'foo': 'bar'}

    @staticmethod
    def load_py():
        '''
        Load from ``CONF_PY`` (``BASE_DIR/config.py``)

        :return: dict
        '''
        logger.warn('method "load_py" not implemented, return dummy')
        return {}


class _Conf:
    __worker = _ConfWorker

    def __getattr__(self, name):
        return self.__worker.get(name)

    def __setattr__(self, name, value):
        self.__worker.set(name, value)

    def __iter__(self):
        raise NotImplemented()


class _Future(Event):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error = False

    def set(self, value):
        super().set()
        self._value = value

    @property
    def result(self):
        if not hasattr(self, '_value'):
            self.wait()
        return self._value

    def set_error(self):
        super().set()
        self.error = True
        self._value = None


class _Message:
    '''
    The message object to communicate with config thread via ``Queue``

    We have two format for message:
    - ('get', name, _Future)
    - ('set', name, value)

    :param method: the action ``get`` or ``set``
    :param str name: the config property name
    :param value: required arg for ``set``
    '''
    def __init__(self, method: 'get' or 'set', name, value=None):
        if method not in ('get', 'set'):
            raise TypeError('Invalide method {}'.format(method))

        self.method = method
        self.name = name
        self.value = _Future() if self.method == 'get' else value

    def __repr__(self):
        return '_Message: ({}, {}, {})'.format(
            self.method, self.name, self.value)


start_conf_thread = _ConfWorker.start_thread

conf = _Conf()
