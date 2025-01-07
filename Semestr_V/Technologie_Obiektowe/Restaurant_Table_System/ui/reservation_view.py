import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from models.reservation import Reservation

import tkinter as tk
from tkinter import ttk
from datetime import datetime

class ReservationView:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager

    def show(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("Manage Reservations")
        self.window.geometry("400x400")

        tk.Label(self.window, text="Table ID:").pack(pady=5)
        self.table_id_var = tk.StringVar()
        table_id_entry = tk.Entry(self.window, textvariable=self.table_id_var)
        table_id_entry.pack(pady=5)

        tk.Label(self.window, text="Date (YYYY-MM-DD):").pack(pady=5)
        self.date_var = tk.StringVar()
        date_entry = tk.Entry(self.window, textvariable=self.date_var)
        date_entry.pack(pady=5)

        tk.Label(self.window, text="Time (HH:MM):").pack(pady=5)
        self.time_var = tk.StringVar()
        time_entry = tk.Entry(self.window, textvariable=self.time_var)
        time_entry.pack(pady=5)

        tk.Label(self.window, text="Customer Name:").pack(pady=5)
        self.customer_name_var = tk.StringVar()
        customer_name_entry = tk.Entry(self.window, textvariable=self.customer_name_var)
        customer_name_entry.pack(pady=5)

        tk.Button(self.window, text="Add Reservation", command=self.add_reservation).pack(pady=10)

        self.reservations_frame = tk.Frame(self.window)
        self.reservations_frame.pack(fill=tk.BOTH, expand=True)
        self.render_reservations()

    def add_reservation(self):
        try:
            table_id = int(self.table_id_var.get())
            date = self.date_var.get()
            time = self.time_var.get()
            customer_name = self.customer_name_var.get()

            datetime.strptime(date, "%Y-%m-%d")
            datetime.strptime(time, "%H:%M")

            reservation = Reservation(table_id, date, time, customer_name)
            self.manager.reservations.append(reservation)

            self.render_reservations()
        except ValueError:
            pass
    def delete_reservation(self, reservation):
        self.manager.reservations.remove(reservation)
        self.render_reservations()

    def render_reservations(self):
        for widget in self.reservations_frame.winfo_children():
            widget.destroy()

        scroll_frame = tk.Frame(self.reservations_frame)
        scroll_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(scroll_frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(scroll_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        sorted_reservations = sorted(
            self.manager.reservations,
            key=lambda res: datetime.strptime(f"{res.date} {res.time}", "%Y-%m-%d %H:%M")
        )

        for res in sorted_reservations:
            reservation_text = f"Table {res.table_id}: {res.date} {res.time} - {res.customer_name}"

            frame = tk.Frame(scrollable_frame)
            frame.pack(fill=tk.X, pady=5)

            tk.Label(frame, text=reservation_text, anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)

            delete_button = tk.Button(frame, text="Delete", command=lambda r=res: self.delete_reservation(r))
            delete_button.pack(side=tk.RIGHT, padx=5)