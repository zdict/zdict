import abc


class DictBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_prompt(self) -> str:
        ...

    def prompt(self):
        return input(self.get_prompt())

    @abc.abstractclassmethod
    def query(self, s: str):
        ...
