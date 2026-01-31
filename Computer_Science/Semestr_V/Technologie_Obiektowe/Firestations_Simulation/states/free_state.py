from .i_states import IStates

class FreeState(IStates):
    def get_state(self, vehicle):
        vehicle.state = FreeState()