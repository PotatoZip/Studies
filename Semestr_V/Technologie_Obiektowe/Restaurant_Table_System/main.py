import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from ui.tables_view import TablesView
from ui.manage_view import ManageView
from models.table import Table
from services.table_stategy import TableStrategy
from states.available_state import AvailableState
from states.dirty_state import DirtyState
from states.occupied_state import OccupiedState
from configuration import TABLE_CONFIGURATION, INITIAL_CHAIR_STOCK

import tkinter as tk
from tkinter import messagebox


class RestaurantApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Restaurant Management System")
        self.root.geometry("800x600")

        self.manager = TableStrategy(TABLE_CONFIGURATION, INITIAL_CHAIR_STOCK)

        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        # Etykieta z liczbą dostępnych dodatkowych krzeseł
        self.chair_stock_label = tk.Label(self.root, text=f"Dostępne dodatkowe krzesełka: {self.manager.chair_stock.get_stock()}")
        self.chair_stock_label.pack(pady=10)

        self.render_table_view()

    def render_table_view(self):
        """Renderuje widok stolików."""
        row = col = 0

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        for table in self.manager.tables:
            button_color = "green" if table.state.__class__.__name__ == "AvailableState" else \
                           "red" if table.state.__class__.__name__ == "OccupiedState" else "yellow"
            table_button = tk.Button(
                self.table_frame,
                text=f"Stół {table.id}\nMiejsca: {table.get_total_seats()}",
                bg=button_color,
                command=lambda t=table: self.open_reservation_view(t)
            )
            table_button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            col += 1
            if col == 5:
                col = 0
                row += 1

        for i in range(5):  # 5 kolumn w gridzie
            self.table_frame.grid_columnconfigure(i, weight=1)

        # Ustawiamy, żeby wszystkie komórki w gridzie miały taką samą wysokość
        for i in range(row + 1):
            self.table_frame.grid_rowconfigure(i, weight=1)


    def open_reservation_view(self, table):
        """Otwiera panel zarządzania stolikiem."""
        reservation_window = tk.Toplevel(self.root)
        reservation_window.title(f"Stół {table.id}")
        reservation_window.geometry("400x300")

        tk.Label(reservation_window, text=f"Stół {table.id} - Stan: {table.state.__class__.__name__}").pack(pady=10)
        tk.Label(reservation_window, text=f"Liczba miejsc: {table.get_total_seats()}").pack(pady=10)

        if table.state.__class__.__name__ == "AvailableState":
            tk.Button(reservation_window, text="Zajmij stolik", command=lambda: self.occupy_table(table, reservation_window)).pack(pady=5)
        elif table.state.__class__.__name__ == "DirtyState":
            tk.Button(reservation_window, text="Zwolnij stolik", command=lambda: self.release_table(table, reservation_window)).pack(pady=5)
        elif table.state.__class__.__name__ == "OccupiedState":
            tk.Button(reservation_window, text="Posprzataj stolik", command=lambda: self.clean_table(table, reservation_window)).pack(pady=5)

        # Dodawanie/odejmowanie krzesełek
        tk.Label(reservation_window, text="Dodatkowe krzesełka:").pack(pady=10)
        tk.Button(reservation_window, text="Dodaj krzesełko", command=lambda: self.add_chair(table)).pack(pady=5)
        tk.Button(reservation_window, text="Usuń wszystkie dodatkowe krzesełka", command=lambda: self.remove_chairs(table)).pack(pady=5)

    def occupy_table(self, table, window):
        table.set_state(OccupiedState())
        self.render_table_view()
        window.destroy()

    def release_table(self, table, window):
        table.set_state(AvailableState())
        self.render_table_view()
        window.destroy()

    def clean_table(self, table, window):
        table.set_state(DirtyState())
        self.render_table_view()
        window.destroy()

    def add_chair(self, table):
        try:
            table.add_chairs(1)
            self.chair_stock_label.config(text=f"Dostępne dodatkowe krzesełka: {self.manager.chair_stock.get_stock()}")
            self.render_table_view()
        except ValueError as e:
            messagebox.showerror("Błąd", str(e))

    def remove_chairs(self, table):
        table.remove_chairs()
        self.chair_stock_label.config(text=f"Dostępne dodatkowe krzesełka: {self.manager.chair_stock.get_stock()}")
        self.render_table_view()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    RestaurantApp().run()