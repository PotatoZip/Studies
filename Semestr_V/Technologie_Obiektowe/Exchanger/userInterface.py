from abc import ABC, abstractmethod

class IUserInterface(ABC):
    @abstractmethod
    def mainLoop(self):
        pass
    
class UserInterface(IUserInterface):

    def mainLoop(self):
        pass
