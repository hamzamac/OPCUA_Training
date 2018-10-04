import abc

class MyABC(abc.ABCMeta):
    #__metaclass__ = abc.ABCMeta #makame class abstract

    @abc.abstractmethod
    def do_something(self):
        pass

    @abc.abstractproperty
    def do_again(self):
        pass