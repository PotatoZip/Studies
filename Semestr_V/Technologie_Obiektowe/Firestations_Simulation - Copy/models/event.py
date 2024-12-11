import random
from states.free_state import FreeState

class Event:
    def __init__(self):
        self.type = None  # PZ, AF, MZ
        self.location = None  # Współrzędne (lat, lon)
        self.complete = False
        self.duration = 0  # Czas trwania zdarzenia
        self.time_elapsed = 0  # Ile czasu minęło
        self.assigned_vehicles = []

    def mark_complete(self):
        self.complete = True
        # for vehicle in self.assigned_vehicles:
        #     vehicle.complete_task()
        for vehicle in self.assigned_vehicles:
            if vehicle.current_event == self:  # Upewniamy się, że pojazd jest przypisany do tego zdarzenia
                vehicle.state = FreeState()  # Zmieniamy stan pojazdu na wolny
                vehicle.current_event = None  # Zwalniamy pojazd z zadania
                vehicle.notify_observers()

    def randomize(self):
        # Losowanie typu zdarzenia
        self.type = random.choices(["PZ", "MZ", "AF"], [0.3, 0.7, 0.05])[0]
        
        # Losowanie współrzędnych zdarzenia w obszarze
        lat = random.uniform(49.95855025648944, 50.154564013341734)
        lon = random.uniform(19.688292482742394, 20.02470275868903)
        self.location = (lat, lon)

        # Ustawienie czasu trwania
        if self.type == "AF":  # Alarm fałszywy
            self.duration = random.randint(1, 3)
        else:  # Pożar lub miejscowe zagrożenie
            self.duration = random.randint(5, 25)

    def progress(self):
        self.time_elapsed += 1
        if self.time_elapsed >= self.duration:
            self.mark_complete()

    def __str__(self):
        # Zwraca przyjazną reprezentację zdarzenia
        return f"Event {self.type} w lokalizacji {self.location}"