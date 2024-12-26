from abc import ABC, abstractmethod

class IState(ABC):
    @abstractmethod
    def get_state(self, table):
        pass