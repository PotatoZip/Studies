from .i_states import IStates

class FreeState(IStates):
    def get_state(self):
        return "free_state"