from interfaces.i_state import IState

class OccupiedState(IState):
    def get_state(self, table):
        table.state = OccupiedState()