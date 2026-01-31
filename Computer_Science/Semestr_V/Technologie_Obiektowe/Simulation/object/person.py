from .memento_person import MementoPerson
import sys
import random
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[1]))

from state.i_state import IState
from state.healty_state import HealtyState
from state.immune_state import ImmunteState
from state.no_symptoms_state import NoSymptomsState
from state.symptoms_state import SymptomsState
from vector.vector_2D import Vector2D

class Person:
    _state : IState
    _position : Vector2D
    _velocity : Vector2D
    _on_screen : bool
    _time_near_unhealthy : int
    _time_near_no_symptoms : int
    _time_to_recover : int
    _time_sick : int
    _max_width : int
    _max_height : int 
    
    def __init__(self, state : IState, x = 0, y = 0, width = 100, height = 100, velocity = 0, onPlane = True, timeNearUnhealthy = 0, timeNearNoSymptoms = 0, timeToRecover = 0, timeSick = 0 ) -> None:
        self._state = state
        self._position = Vector2D(x, y)
        if velocity == 0:
            x = (random.uniform(-1, 1)*2.5)/25
            y = (random.uniform(-1, 1)*2.5)/25
            self._velocity = Vector2D(x, y)
        if isinstance(velocity, Vector2D):
            self._velocity = velocity
        self._on_screen = onPlane
        self._time_near_unhealthy = timeNearUnhealthy
        self._time_near_no_symptoms = timeNearNoSymptoms
        self._time_sick = timeSick
        if timeToRecover == 0:
            self._time_to_recover = (20 + random.randint(0, 10)) *25
        else:
            self._time_to_recover = timeToRecover
        self._max_width = width
        self._max_height = height
    
    def move(self):
        if random.random() < 0.01:
            x = (random.uniform(-1, 1)*2.5)/25
            y = (random.uniform(-1, 1)*2.5)/25
            self._velocity = Vector2D(x, y)
        self._position = self._position + self._velocity
    
    def get_on_screen(self):
        if self._position.get_x() < 0 or self.get_x() > self._max_width or self.get_y() < 0 or self.get_y() > self._max_height:
            if random.random() < 0.5:
                self._velocity.set_x(-self._velocity.get_x())
                self._velocity.set_y(-self._velocity.get_y())            
            else:
                self._on_screen = False
        return self._on_screen
    
    def when_near_unhealthy(self, other: 'Person'):
        if isinstance(self._state, HealtyState) and (isinstance(other._state, SymptomsState) or isinstance(other._state, NoSymptomsState)):
            if isinstance(other._state, SymptomsState):
                self._time_near_unhealthy += 1
            if isinstance(other._state, NoSymptomsState):
                self._time_near_no_symptoms += 1
            return True
        
    def distance(self, other: 'Person'):
        return self._position.distance(other._position)
    
    def is_near(self, other: 'Person'):
        return self.distance(other) < 3.0
    
    def check_state(self):
        if isinstance(self._state, HealtyState):
            if self._time_near_unhealthy > 50:
                if random.random() < 0.5:
                    self._state = NoSymptomsState()
                    return
                else:
                    self._state = SymptomsState()
                    return
            elif self._time_near_no_symptoms > 50:
                if random.random() <= 0.5:
                    if random.random() <= 0.5:
                        self._state = NoSymptomsState()
                        return
                    else:
                        self._state = SymptomsState() 
                        return
                else:
                    self._state = HealtyState()
                    self._time_near_no_symptoms = 0
    
    def check_recover(self):
        if isinstance(self._state, SymptomsState) or isinstance(self._state, NoSymptomsState):
            self._time_sick += 1
            if self._time_sick > self._time_to_recover:
                self._state = ImmunteState()
 
    def save_to_memento(self):
        return MementoPerson(self._state, self._position, self._velocity, self._on_screen, self._time_near_unhealthy, self._time_near_no_symptoms, self._time_to_recover, self._max_width, self._max_height)
    
    def restore_from_memento(self, memento: MementoPerson):
        state_instance = HealtyState()
        if memento.get_state() == ImmunteState().get_state():
            state_instance = ImmunteState()
        elif memento.get_state() == SymptomsState().get_state():
            state_instance = SymptomsState()
        elif memento.get_state() == NoSymptomsState().get_state():
            state_instance = NoSymptomsState()
        self._state = state_instance
        self._position = memento.get_position()
        self._velocity = memento.get_velocity()
        self._on_screen = memento.get_on_screen()
        self._time_near_unhealthy = memento.get_time_near_unhealthy()
        self._time_near_no_symptoms = memento.get_time_near_no_symptoms()
        self._time_to_recover = memento.get_time_to_recover()
        self._max_width = memento.get_max_width()
        self._max_height = memento.get_max_height()

    def set_state(self, state: IState):
        self._state = state
    
    def get_color(self):
        return self._state.get_state()
    
    def set_position(self, x, y):
        self._position = Vector2D(x, y)
    
    def get_position(self):
        return self._position
    
    def get_x(self):
        return self._position.get_x()
    
    def get_y(self):
        return self._position.get_y()
    
    def get_velocity(self):
        return self._velocity
    
    def set_velocity(self, x, y):
        self._velocity = Vector2D(x, y)
        
    def get_state(self):
        return self._state

    def set_on_screen(self, on_screen):
        self._on_screen = on_screen

    def set_time_near_unhealthy(self, time_near_unhealthy):
        self._time_near_unhealthy = time_near_unhealthy

    def set_time_near_no_symptoms(self, time_near_no_symptoms):
        self._time_near_no_symptoms = time_near_no_symptoms

    def set_time_to_recover(self, time_to_recover):
        self._time_to_recover = time_to_recover

    def set_time_sick(self, time_sick):
        self._time_sick = time_sick

    def set_max_width(self, max_width):
        self._max_width = max_width

    def set_max_height(self, max_height):
        self._max_height = max_height
    
    def get_time_near_unhealthy(self):
        return self._time_near_unhealthy

    