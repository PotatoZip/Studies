from .i_state import IState

class NoSymptomsState(IState):
    def get_state(self):
        return "yellow"