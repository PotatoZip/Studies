import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from models.fire_station import FireStation
from models.event import Event
from observers.logger import Logger
from iteration.iterator import Iterator
from dispatcher.dispatcher_strategy import FireDispatchStrategy, HazardDispatchStrategy
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Map:
    corner_3 = 50.154564013341734
    corner_4 = 49.95855025648944
    corner_1 = 20.02470275868903
    corner_2 = 19.688292482742394

    stations_location = {
        "JRG1": [50.0599179817761, 19.943109097898308],
        "JRG2": [50.03367378422457, 19.935677587243156],
        "JRG3": [50.07558843771017, 19.887066835538878],
        "JRG4": [50.037607106477815, 20.005775043445905],
        "JRG5": [50.092112896692576, 19.920375568078363],
        "JRG6": [50.01600677090119, 20.01560115206121],
        "JRG7": [50.09403344711918, 19.977527923870664],
        "JRG_Skawina": [49.968341021285674, 19.79928999293016],
        "JRG_PSP": [50.07711317778578, 20.032658871795807],
        "LSB_Balice": [50.07327060533678, 19.80488126069325]
    }

    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.fig.suptitle("Fire Stations Simulation", fontsize=16)
        self.ax.set_xlim(self.corner_2, self.corner_1)
        self.ax.set_ylim(self.corner_4, self.corner_3)

        self.fire_stations = self.create_fire_stations()
        self.skkm = Logger(self.fire_stations)
        self.fire_dispatcher = FireDispatchStrategy()
        self.hazard_dispatcher = HazardDispatchStrategy()
        self.events = []
        self.step_count = 0
        self.event_interval = 3

    def create_fire_stations(self):
        stations = []
        for name, location in self.stations_location.items():
            stations.append(FireStation(name, location))
        return stations

    def start_simulation(self, steps=10000):
        self.ani = FuncAnimation(self.fig, self.animate, frames=steps, interval=500, repeat=False)
        plt.show()

    def animate(self, i):
        self.step_count += 1
        if self.step_count % self.event_interval == 0:
            event = Event()
            event.randomize()
            self.skkm.log_event(event)

            if event.type == "PZ":
                vehicles_assigned = self.fire_dispatcher.dispatch(event, self.fire_stations)
            elif event.type == "MZ":
                vehicles_assigned = self.hazard_dispatcher.dispatch(event, self.fire_stations)
            else:
                vehicles_assigned = []

            self.events.append(event)

        self.update_simulation()
        self.display_map()

    def update_simulation(self):
        event_iterator = self.get_event_iterator()
    
        # for event in self.events:
        #     if not event.complete:
        #         event.progress()

        for event in event_iterator:
            if not event.complete:
                event.progress()

        for event in self.events:
            if event.complete:
                for vehicle in event.assigned_vehicles:
                    vehicle.complete_task() 

        self.cleanup_completed_events()

        for station in self.fire_stations:
            for vehicle in station.vehicles:
                vehicle.update_state()

    def cleanup_completed_events(self):
        self.events = [event for event in self.events if not event.complete]

    def get_event_iterator(self):
        return Iterator(self.events)

    def display_map(self):
        self.ax.clear()
        self.ax.set_xlim(self.corner_2, self.corner_1)
        self.ax.set_ylim(self.corner_4, self.corner_3)

        for station in self.fire_stations:
            x, y = station.location
            self.ax.plot(y, x, 'ro', label="Fire Stations:")

        for event in self.events:
            if not event.complete:
                x, y = event.location
                if event.type == "PZ":
                    self.ax.plot(y, x, 'bo')
                elif event.type == "MZ":
                    self.ax.plot(y, x, 'go')
                elif event.type == "AF":
                    self.ax.plot(y, x, 'yo')

        self.ax.legend(handles=[
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='r', markersize=10, label="Fire Stations"),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='b', markersize=10, label="Fire"),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='g', markersize=10, label="Local event"),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='y', markersize=10, label="False alarm")
        ], loc="upper left")

        plt.draw()