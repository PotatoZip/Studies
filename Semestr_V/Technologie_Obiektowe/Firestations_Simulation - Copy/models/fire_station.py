from states.free_state import FreeState
from states.busy_state import BusyState
from states.returning_state import ReturningState
from .vehicle import Vehicle
from dispatcher.i_dispatcher_strategy import IDispatcher

class FireStation:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.vehicles = [Vehicle(i) for i in range(5)]
        self.state = FreeState()
        self.dispatch_strategy = None

    def set_dispatch_strategy(self, strategy: IDispatcher):
        self.dispatch_strategy = strategy

    def get_free_vehicles(self):
        return [vehicle for vehicle in self.vehicles if vehicle.is_free()]

    def dispatch_vehicle(self, event):
        for vehicle in self.vehicles:
            if vehicle.is_free():
                vehicle.assign_task(event)
                return vehicle
        return None
    
    def add_observer(self, observer):
        # Dodajemy obserwatora, który będzie monitorował jednostki w stacji
        for vehicle in self.vehicles:
            vehicle.add_observer(observer)

    def has_free_vehicle(self):
        return any(vehicle.is_free() for vehicle in self.vehicles)
    
    def __str__(self):
        return f"{self.name} at {self.location}"
    
    def __repr__(self):
        return self.__str__()