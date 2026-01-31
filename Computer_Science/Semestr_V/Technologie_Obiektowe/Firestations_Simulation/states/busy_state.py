from .i_states import IStates

class BusyState(IStates):
    def get_state(self, vehicle):
        vehicle.state = BusyState()