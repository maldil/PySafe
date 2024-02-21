from abc import ABC, abstractmethod


class IError(ABC):
    def __init__(self, key):
        self.key = key

    @abstractmethod
    def get_key(self):
        return self.key

    @abstractmethod
    def get_line_number(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __ne__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass


