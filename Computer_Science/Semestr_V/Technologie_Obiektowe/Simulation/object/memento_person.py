import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from state.i_state import IState
from state.healty_state import HealtyState
from state.immune_state import ImmunteState
from state.no_symptoms_state import NoSymptomsState
from state.symptoms_state import SymptomsState
from vector.vector_2D import Vector2D

class MementoPerson:
    _state : IState
    _position : Vector2D
    _velocity : Vector2D
    _on_screen : bool
    _time_near_unhealthy : int
    _time_near_no_symptoms : int
    _time_to_recover : int
    _time_sick : int
    _max_width = float
    _max_height = float

    def __init__(self, IState, position, velocity, onPlane, timeNearUnhealthy, timeNearNoSymptoms, timeToRecover, maxwidth, maxheight) -> None:
        self._state = IState
        self._position = position
        self._velocity = velocity
        self._on_screen = onPlane
        self._time_near_unhealthy = timeNearUnhealthy
        self._time_near_no_symptoms = timeNearNoSymptoms
        self._time_to_recover = timeToRecover
        self._max_width = maxwidth
        self._max_height = maxheight

    def get_state(self):
        return self._state.get_state()
    
    def get_position(self):
        return self._position
    
    def get_velocity(self):
        return self._velocity
    
    def get_on_screen(self):
        return self._on_screen
    
    def get_time_near_unhealthy(self):
        return self._time_near_unhealthy
    
    def get_time_near_no_symptoms(self):
        return self._time_near_no_symptoms
    
    def get_time_to_recover(self):
        return self._time_to_recover
    
    def get_max_width(self):
        return self._max_width
    
    def get_max_height(self):
        return self._max_height
    
    