from states.i_states import IStates
from states.busy_state import BusyState
from states.free_state import FreeState
from states.returning_state import ReturningState

class Vehicle:
    def __init__(self, name):
        self.state = FreeState()
        self.current_event = None
        self._observers = []
        self.name = name

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update(self)

    def is_free(self):
        return isinstance(self.state, FreeState)
    
    def assign_task(self, event):
        self.state = BusyState()
        self.current_event = event
        event.assigned_vehicles.append(self)
        self.notify_observers()

    def complete_task(self):
        if self.current_event:
            self.current_event.mark_complete()
        self.state = FreeState()
        self.current_event = None
        self.notify_observers()

    def update_state(self):
        self.state.get_state(self)

    def __str__(self):
        return f"{self.name}"
