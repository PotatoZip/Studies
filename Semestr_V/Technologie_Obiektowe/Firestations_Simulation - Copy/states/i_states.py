from abc import ABC, abstractmethod

class IStates(ABC):
    @abstractmethod
    def get_state(self, vehicle):
        pass