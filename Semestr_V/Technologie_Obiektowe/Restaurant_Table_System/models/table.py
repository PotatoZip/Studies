import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from interfaces.i_state import IState
from states.available_state import AvailableState
from states.dirty_state import DirtyState
from states.occupied_state import OccupiedState

class Table:
    def __init__(self, table_id, seats, chair_supply):
        self.id = table_id
        self.base_seats = seats
        self.chair_supply = chair_supply
        self.extra_chairs = 0
        self.state:IState = AvailableState()

    def add_chairs(self, amount):
        self.extra_chairs += self.chair_supply.take_chairs(amount)

    def remove_chairs(self):
        self.chair_supply.return_chairs(self.extra_chairs)
        self.extra_chairs = 0

    def get_total_seats(self):
        return self.base_seats + self.extra_chairs
    
    def set_state(self, state):
        self.state = state