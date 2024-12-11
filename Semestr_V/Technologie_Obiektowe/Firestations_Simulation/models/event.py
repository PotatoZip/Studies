import random
from states.free_state import FreeState

class Event:
    def __init__(self):
        self.type = None
        self.location = None
        self.complete = False
        self.duration = 0
        self.time_elapsed = 0
        self.assigned_vehicles = []

    def mark_complete(self):
        self.complete = True

        for vehicle in self.assigned_vehicles:
            if vehicle.current_event == self:
                vehicle.state = FreeState()
                vehicle.current_event = None
                vehicle.notify_observers()

    def randomize(self):
        self.type = random.choices(["PZ", "MZ", "AF"], [0.3, 0.7, 0.05])[0]
        
        lat = random.uniform(49.95855025648944, 50.154564013341734)
        lon = random.uniform(19.688292482742394, 20.02470275868903)
        self.location = (lat, lon)

        if self.type == "AF":
            self.duration = random.randint(1, 3)
        else:
            self.duration = random.randint(5, 25)

    def progress(self):
        self.time_elapsed += 1
        if self.time_elapsed >= self.duration:
            self.mark_complete()

    def __str__(self):
        return f"Event {self.type} w lokalizacji {self.location}"