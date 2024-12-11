from .i_states import IStates

class ReturningState(IStates):
    def get_state(self, vehicle):
        vehicle.state = ReturningState()