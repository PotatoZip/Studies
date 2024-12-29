from interfaces.i_state import IState

class AvailableState(IState):
    def get_state(self, table):
        table.state = AvailableState()