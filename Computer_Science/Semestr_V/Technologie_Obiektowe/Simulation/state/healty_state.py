from .i_state import IState

class HealtyState(IState):
    def get_state(self):
        return "green"
    