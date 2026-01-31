import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
import random
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from object.care_taker_person import CareTakerPerson
from object.person import Person
from state.i_state import IState
from state.healty_state import HealtyState
from state.immune_state import ImmunteState
from state.no_symptoms_state import NoSymptomsState
from state.symptoms_state import SymptomsState
from vector.vector_2D import Vector2D

class Simulation:
    max_x = 100
    max_y = 100
    numofpeople = 100
    persons = []
    xdata, ydata, colors = [], [], []
    last_time = 0
    use_immunity = False
    
    def __init__(self, max_x, max_y, numofpeople) -> None:
        self.max_x = max_x
        self.max_y = max_y
        self.numofpeople = numofpeople
        self.fig, self.ax = plt.subplots()
        self.fig.suptitle("Pandemic simulation", fontsize=16)
        self.points, = self.ax.plot([], [], 'o')
        self.xdata, self.ydata = [], []
        self.ani = FuncAnimation(self.fig, self.update, frames=np.arange(0, 10000, 1),
                                 init_func=self.init, blit=True, interval=40)
        
    def init(self):
        self.ax.set_xlim(0, self.max_x)
        self.ax.set_ylim(0, self.max_y)
        return self.points,
    
    
    def update(self, frame):
        if len(self.persons) < self.numofpeople:
            for i in range(self.numofpeople - len(self.persons)):
                self.add_person()
        for person in self.persons:
            person.move()
            if not person.get_on_screen():
                self.persons.remove(person)
                self.add_person()
        for person in self.persons:
            for another in self.persons:
                if person.is_near(another) and person != another:
                    if person.when_near_unhealthy(another):
                        break
            person.check_state()
            person.check_recover()
        self.xdata.clear()
        self.ydata.clear()
        self.colors.clear()
        for person in self.persons:
            if isinstance(person, Person):
                self.xdata.append(person.get_x())
                self.ydata.append(person.get_y())
                self.colors.append(person.get_color())
        self.points = self.ax.scatter(self.xdata, self.ydata, c=self.colors)
        return self.points,
    

    def show_animation(self):
        plt.subplots_adjust(bottom=0.2)

        button_ax1 = plt.axes([0.3, 0.05, 0.2, 0.075])
        button1 = Button(button_ax1, 'No Immunity')
        button_ax2 = plt.axes([0.1, 0.05, 0.2, 0.075])
        button2 = Button(button_ax2, 'With Immunity')
        
        save_ax = plt.axes([0.5, 0.05, 0.2, 0.075])
        save_button = Button(save_ax, 'Save')
        restore_ax = plt.axes([0.7, 0.05, 0.2, 0.075])
        restore_button = Button(restore_ax, 'Restore')

        def on_button1_clicked(event):
            self.use_immunity = False
            self.start_simulation()

        def on_button2_clicked(event):
            self.use_immunity = True
            self.start_simulation()

        def on_save_clicked(event):
            care_taker = CareTakerPerson()
            care_taker.backup(self.persons)
            care_taker.save()

        def on_restore_clicked(event):
            care_taker = CareTakerPerson()
            care_taker.restore()
            self.persons.clear()
            mementos = care_taker.get_mementos()
            for memento in mementos:
                p = Person(NoSymptomsState())
                p.restore_from_memento(memento)
                self.persons.append(p)

        button1.on_clicked(on_button1_clicked)
        button2.on_clicked(on_button2_clicked)
        save_button.on_clicked(on_save_clicked)
        restore_button.on_clicked(on_restore_clicked)
        plt.show()

    def start_simulation(self):
        self.persons.clear()
        self.generate_population(self.numofpeople)

    def generate_population(self, n):
        for i in range(n):
            x = random.randint(0, self.max_x)
            y = random.randint(0, self.max_y)
            if self.use_immunity and random.random() < 0.1:  # 10% odporności
                p = Person(ImmunteState(), x, y, self.max_x, self.max_y)
            else:
                p = Person(HealtyState(), x, y, self.max_x, self.max_y)
            self.persons.append(p)
            self.xdata.append(x)
            self.ydata.append(y)
            self.colors.append(p.get_color())

    def add_person(self):
        x: int
        y: int
        p: Person
        propability = random.random()
        if propability < 0.25:
            x = 0
            y = random.randint(0, self.max_y)
        elif propability < 0.5:
            x = random.randint(0, self.max_x)
            y = 0
        elif propability < 0.75:
            x = self.max_x
            y = random.randint(0, self.max_y)
        else:
            x = random.randint(0, self.max_x)
            y = self.max_y

        if random.random() < 0.1:  # 10% szans na bycie chorym
            if random.random() < 0.5:
                p = Person(NoSymptomsState(), x, y, self.max_x, self.max_y)
            else:
                p = Person(SymptomsState(), x, y, self.max_x, self.max_y)
        elif self.use_immunity and random.random() < 0.1:  # 10% szans na odporność
            p = Person(ImmunteState(), x, y, self.max_x, self.max_y)
        else:
            p = Person(HealtyState(), x, y, self.max_x, self.max_y)
        self.persons.append(p)


if __name__ == "__main__":
    sim = Simulation(10, 10, 40)
    sim.show_animation()

    