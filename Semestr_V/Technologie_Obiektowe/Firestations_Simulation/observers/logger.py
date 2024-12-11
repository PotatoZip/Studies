from .i_logger import ILogger

class Logger(ILogger):
    def __init__(self, stations):
        self.stations = stations
        self.events = []
        self.vehicles = []
        self._subscribe_to_stations()

    def _subscribe_to_stations(self):
        for station in self.stations:
            for vehicle in station.vehicles:
                vehicle.add_observer(self)

    def log_event(self, event):
        print(f"\nZdarzenie: {event.type} w {event.location}!")

        for station in self.stations:
            print(f"Jednostka: {station.name}")
            for vehicle in station.vehicles:
                if vehicle.is_free():
                    print(f"  {vehicle} jest wolny")
                else:
                    print(f"  {vehicle} jest zajęty, przypisany do zdarzenia: {vehicle.current_event}")
        print("\n")

    def update(self, event):
        pass