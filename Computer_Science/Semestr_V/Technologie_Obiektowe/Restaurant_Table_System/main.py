import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from ui.tables_view import TablesView
from services.table_stategy import TableStrategy
from configuration import TABLE_CONFIGURATION, INITIAL_CHAIR_STOCK

import tkinter as tk

class RestaurantApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Restaurant Management System")
        self.root.geometry("800x600")

        self.manager = TableStrategy(TABLE_CONFIGURATION, INITIAL_CHAIR_STOCK)
        self.table_view = TablesView(self.manager, self.root)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = RestaurantApp()
    app.run()