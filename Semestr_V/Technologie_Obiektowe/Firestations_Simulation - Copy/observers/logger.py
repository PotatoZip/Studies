from .i_logger import ILogger

class Logger(ILogger):
    def __init__(self, stations):
        self.stations = stations  # Lista stacji PSP
        self.events = []  # Zdarzenia, które są monitorowane
        self.vehicles = []
        self._subscribe_to_stations()

    # def dispatch(self, event):
    #     available_stations = [station for station in self.stations if station.has_free_vehicle()]
    #     vehicles_assigned = []
    #     for station in available_stations[:3]:  # Przypisanie maksymalnie 3 jednostek
    #         vehicle = station.dispatch_vehicle(event)
    #         vehicles_assigned.append(vehicle)
    #     return vehicles_assigned

    def _subscribe_to_stations(self):
        # Subskrybujemy się na zmiany w jednostkach (pojazdach)
        for station in self.stations:
            for vehicle in station.vehicles:
                vehicle.add_observer(self)

    def update(self, vehicle):
        # Informacja o stanie pojazdu
        if vehicle.is_free():
            # print(f"  {vehicle} jest wolny.")
            pass
        else:
            # print(f"  {vehicle} jest zajęty, przypisany do zdarzenia: {vehicle.current_event}")
            pass

    def log_event(self, event):
        # Informacja o rozpoczęciu zdarzenia
        print(f"\nZdarzenie: {event.type} w {event.location}!")

        # Wypisz dostępność pojazdów
        for station in self.stations:
            print(f"Jednostka: {station.name}")
            for vehicle in station.vehicles:
                if vehicle.is_free():
                    print(f"  {vehicle} jest wolny")
                else:
                    print(f"  {vehicle} jest zajęty, przypisany do zdarzenia: {vehicle.current_event}")

    def log_event_dispatch(self, event, vehicles_assigned):
        # print(f"Zdarzenie {event.type} w {event.location} zostało obsłużone przez jednostki: ")
        # for vehicle in vehicles_assigned:
        #     print(f"  {vehicle} przypisany do zdarzenia")
        pass