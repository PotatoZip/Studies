import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from interfaces.i_state import IState

class AvailableState(IState):
    def get_state(self, table):
        table.state = AvailableState()