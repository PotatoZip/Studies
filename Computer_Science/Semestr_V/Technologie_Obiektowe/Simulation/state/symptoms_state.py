from .i_state import IState

class SymptomsState(IState):
    def get_state(self):
        return "red"