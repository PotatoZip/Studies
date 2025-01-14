import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from models.reservation import Reservation

import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime, timedelta
from tkinter import messagebox
from collections import defaultdict

class ReservationView:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager

    def show(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("Manage Reservations")
        self.window.geometry("600x600")

        add_frame = tk.LabelFrame(self.window, text="Add New Reservation", font=("Arial", 12, "bold"))
        add_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(add_frame, text="Table ID:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.table_id_var = tk.StringVar()
        tk.Entry(add_frame, textvariable=self.table_id_var, width=15).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(add_frame, text="Date (YYYY-MM-DD):", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.date_var = tk.StringVar()
        tk.Entry(add_frame, textvariable=self.date_var, width=15).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(add_frame, text="Start Time (HH:MM):", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.start_time_var = tk.StringVar()
        tk.Entry(add_frame, textvariable=self.start_time_var, width=15).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(add_frame, text="End Time (HH:MM):", font=("Arial", 10)).grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.end_time_var = tk.StringVar()
        tk.Entry(add_frame, textvariable=self.end_time_var, width=15).grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(add_frame, text="Customer Name:", font=("Arial", 10)).grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.customer_name_var = tk.StringVar()
        tk.Entry(add_frame, textvariable=self.customer_name_var, width=15).grid(row=4, column=1, padx=5, pady=5, sticky="w")

        tk.Button(
            add_frame,
            text="Add Reservation",
            font=("Arial", 10, "bold"),
            command=self.add_reservation,
            bg="#4CAF50",
            fg="white"
        ).grid(row=5, column=0, columnspan=2, pady=10)

        self.calendar_frame = tk.LabelFrame(self.window, text="Select Date", font=("Arial", 12, "bold"))
        self.calendar_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.render_calendar()

    def render_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.calendar = Calendar(
            self.calendar_frame,
            selectmode='day',
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day,
            font=("Arial", 10),
            date_pattern="mm/dd/yyyy"
        )
        self.calendar.pack(pady=10)

        tk.Button(
            self.calendar_frame,
            text="Show Reservations",
            font=("Arial", 10, "bold"),
            command=self.show_reservations_window,
            bg="#2196F3",
            fg="white"
        ).pack(pady=10)

    def add_reservation(self):
        try:
            table_id = int(self.table_id_var.get())
            date_input = self.date_var.get()
            start_time = self.start_time_var.get()
            end_time = self.end_time_var.get()
            customer_name = self.customer_name_var.get()

            selected_date = self.calendar.selection_get()
            selected_date_str = selected_date.strftime("%m/%d/%Y")
            dt = datetime.strptime(selected_date_str, "%m/%d/%Y")
            formatted_date = dt.strftime("%Y-%m-%d")

            datetime.strptime(formatted_date, "%Y-%m-%d")
            datetime.strptime(start_time, "%H:%M")
            datetime.strptime(end_time, "%H:%M")

            reservation = Reservation(table_id, formatted_date, start_time, end_time, customer_name)
            self.manager.reservations.append(reservation)

            messagebox.showinfo("Success", f"Reservation added for Table {table_id} on {formatted_date}.")
            self.render_calendar()

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid date/time format! Details:\n{e}")

    def show_reservations_window(self):
        selected_date = self.calendar.selection_get()
        formatted_date = selected_date.strftime("%Y-%m-%d")

        reservations_window = tk.Toplevel(self.window)
        reservations_window.title(f"Reservations for {formatted_date}")
        reservations_window.geometry("600x500")

        reservations_frame = tk.Frame(reservations_window)
        reservations_frame.pack(fill=tk.BOTH, expand=True)

        reservations_for_day = [r for r in self.manager.reservations if r.date == formatted_date]

        if not reservations_for_day:
            tk.Label(
                reservations_frame,
                text=f"No reservations for {formatted_date}.",
                font=("Arial", 12, "italic")
            ).pack(pady=10)
            return

        table_dict = defaultdict(list)
        for r in reservations_for_day:
            table_dict[r.table_id].append(r)

        for table_id in sorted(table_dict.keys()):
            table_frame = tk.LabelFrame(
                reservations_frame,
                text=f"Table {table_id}",
                bd=2,
                relief=tk.RIDGE,
                font=("Arial", 10, "bold")
            )
            table_frame.pack(fill=tk.X, pady=5, padx=5)

            table_dict[table_id].sort(key=lambda x: x.start_time)

            for res in table_dict[table_id]:
                row_frame = tk.Frame(table_frame)
                row_frame.pack(fill=tk.X, anchor="w", padx=10, pady=2)

                res_text = f"{res.start_time} - {res.end_time} : {res.customer_name}"
                tk.Label(row_frame, text=res_text, font=("Arial", 10)).pack(side=tk.LEFT, fill=tk.X, expand=True)

                del_btn = tk.Button(
                    row_frame,
                    text="Delete",
                    font=("Arial", 9, "bold"),
                    bg="#f44336",
                    fg="white",
                    command=lambda r=res: self.delete_reservation_in_window(r, reservations_window)
                )
                del_btn.pack(side=tk.RIGHT, padx=5)

    def delete_reservation_in_window(self, reservation, reservations_window):
        if reservation in self.manager.reservations:
            self.manager.reservations.remove(reservation)
        reservations_window.destroy()
        self.show_reservations_window()