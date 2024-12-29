import tkinter as tk
from tkinter import messagebox

from states.available_state import AvailableState
from states.dirty_state import DirtyState
from states.occupied_state import OccupiedState

class ManageView:
    def __init__(self, root, table, manager, tables_view):
        self.table = table
        self.manager = manager
        self.tables_view = tables_view

        self.window = tk.Toplevel(root)
        self.window.title(f"Table {table.id}")
        self.window.geometry("400x650")

        self.details_frame = tk.Frame(self.window)
        self.details_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.update_reservation_window()

    def update_reservation_window(self):
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        header_frame = tk.Frame(self.details_frame)
        header_frame.pack(pady=10, fill=tk.X)

        tk.Label(header_frame, text=f"Table {self.table.id}", font=("Arial", 16, "bold")).pack(side=tk.TOP, pady=5)
        tk.Label(header_frame, text=f"State: {self.table.state.__class__.__name__}", font=("Arial", 12)).pack(side=tk.TOP, pady=2)
        tk.Label(header_frame, text=f"Seats count: {self.table.get_total_seats()}", font=("Arial", 12)).pack(side=tk.TOP, pady=2)

        actions_frame = tk.LabelFrame(self.details_frame, text="Actions", font=("Arial", 12, "bold"))
        actions_frame.pack(pady=10, padx=10, fill=tk.X)

        if self.table.state.__class__.__name__ == "AvailableState":
            tk.Button(actions_frame, text="Take Table", command=lambda: self.occupy_table()).pack(pady=5, fill=tk.X)
        elif self.table.state.__class__.__name__ == "DirtyState":
            tk.Button(actions_frame, text="Release Table", command=lambda: self.release_table()).pack(pady=5, fill=tk.X)
        elif self.table.state.__class__.__name__ == "OccupiedState":
            tk.Button(actions_frame, text="Clean Table", command=lambda: self.clean_table()).pack(pady=5, fill=tk.X)

        chairs_frame = tk.LabelFrame(self.details_frame, text="Extra Chairs", font=("Arial", 12, "bold"))
        chairs_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Button(chairs_frame, text="Add Chair", command=self.add_chair).pack(pady=5, fill=tk.X)
        tk.Button(chairs_frame, text="Remove All Chairs", command=self.remove_chairs).pack(pady=5, fill=tk.X)

        order_frame = tk.LabelFrame(self.details_frame, text="Order Details", font=("Arial", 12, "bold"))
        order_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        note_text = tk.Text(order_frame, height=10, wrap=tk.WORD, font=("Arial", 10))
        note_text.insert(tk.END, self.table.note)
        note_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        tk.Button(order_frame, text="Save Order", command=lambda: self.save_note(note_text.get("1.0", tk.END).strip()), bg="blue", fg="white").pack(pady=5, fill=tk.X)
        tk.Button(order_frame, text="Delete Order", command=lambda: self.delete_note(), bg="red", fg="white").pack(pady=5, fill=tk.X)
            
    def add_chair(self):
        try:
            self.table.add_chairs(1)
            self.tables_view.update_chair_stock_label()
            self.tables_view.render_table_view()
            self.update_reservation_window()
        except ValueError as e:
            messagebox.showerror("Błąd", str(e))

    def remove_chairs(self):
        self.table.remove_chairs()
        self.tables_view.render_table_view()
        self.tables_view.update_chair_stock_label()

    def save_note(self, note):
        self.table.set_note(note)

    def delete_note(self):
        self.table.set_note("")
        self.update_reservation_window()

    def occupy_table(self):
        self.table.set_state(OccupiedState())
        self.tables_view.render_table_view()
        self.window.destroy()

    def release_table(self):
        self.table.set_state(AvailableState())
        self.tables_view.render_table_view()
        self.window.destroy()

    def clean_table(self):
        self.table.set_state(DirtyState())
        self.tables_view.render_table_view()
        self.window.destroy()
