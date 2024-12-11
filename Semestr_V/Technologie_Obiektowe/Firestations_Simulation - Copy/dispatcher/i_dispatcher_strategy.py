from abc import ABC, abstractmethod

class IDispatcher(ABC):
    @abstractmethod
    def dispatch(self, event, stations):
        pass
    