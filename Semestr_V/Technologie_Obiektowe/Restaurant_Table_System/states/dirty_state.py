import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from interfaces.i_state import IState

class DirtyState(IState):
    def get_state(self, table):
        table.state = DirtyState()