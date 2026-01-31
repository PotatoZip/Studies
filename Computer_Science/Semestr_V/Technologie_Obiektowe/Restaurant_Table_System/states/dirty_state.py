from interfaces.i_state import IState

class DirtyState(IState):
    def get_state(self, table):
        table.state = DirtyState()