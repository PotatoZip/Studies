import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from services.chair_supply import ChairSupply
from models.table import Table

class TableStrategy:
    def __init__(self, table_config, init_chair_stock):
        self.chair_stock = ChairSupply(init_chair_stock)
        self.tables = [
            Table(table_id, seats, self.chair_stock) for table_id, seats in table_config.items()
        ]

    def get_table(self, table_id):
        return next((table for table in self.tables if table.id == table_id), None)