import abc

class BanMethod(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def ban(self, address):
        pass

    @abc.abstractmethod
    def unban(self, address):
        pass