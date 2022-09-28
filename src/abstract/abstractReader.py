import abc

class Reader(metaclass=abc.ABCMeta):
    

    @abc.abstractmethod
    def __next__(self):
        pass

    @abc.abstractmethod
    def __iter__(self):
        pass
