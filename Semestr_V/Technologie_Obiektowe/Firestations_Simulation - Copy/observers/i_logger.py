from abc import ABC, abstractmethod

class ILogger(ABC):
    @abstractmethod
    def update(self, event):
        pass