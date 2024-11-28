from .i_states import IStates

class BusyState(IStates):
    def get_state(self):
        return "busy_state"