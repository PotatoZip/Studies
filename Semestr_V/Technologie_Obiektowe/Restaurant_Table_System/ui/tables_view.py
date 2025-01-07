import tkinter as tk
import datetime
from ui.manage_view import ManageView
from ui.orders_view import OrdersView
from ui.reservation_view import ReservationView

class TablesView:
    def __init__(self, manager, root):
        self.manager = manager
        self.root = root

        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        self.chair_stock_label = tk.Label(self.root, text=f"Extra chairs count: {self.manager.chair_stock.get_stock()}")
        self.chair_stock_label.pack(pady=10)

        self.render_table_view()
        self.update_table_colors()

    def render_table_view(self):
        row = col = 0

        current_time = datetime.datetime.now()

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        for table in self.manager.tables:
            button_color = "green" if table.state.__class__.__name__ == "AvailableState" else \
                           "red" if table.state.__class__.__name__ == "OccupiedState" else "yellow"
            
            for reservation in self.manager.reservations:
                if reservation.table_id == table.id:
                    res_time = datetime.datetime.strptime(f"{reservation.date} {reservation.time}", "%Y-%m-%d %H:%M")
                    time_diff = (res_time - current_time).total_seconds()

                    if 0 < time_diff <= 3600:
                        button_color = "orange"

            table_button = tk.Button(
                self.table_frame,
                text=f"Table {table.id}\nChairs: {table.get_total_seats()}",
                bg=button_color,
                command=lambda t=table: self.open_manage_view(t)
            )
            table_button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            col += 1
            if col == 5:
                col = 0
                row += 1

        view_orders_button = tk.Button(self.table_frame, text="View All Orders", bg="grey", command=self.view_all_orders)
        view_orders_button.grid(row=row, column=0, padx=10, pady=10, sticky="nsew")

        view_reservations_button = tk.Button(
            self.table_frame,
            text="Manage Reservations",
            bg="blue",
            fg="white",
            command=self.open_reservation_view
        )
        view_reservations_button.grid(row=row + 1, column=0, columnspan=5, pady=10, sticky="nsew")


        for i in range(5):
            self.table_frame.grid_columnconfigure(i, weight=1)

        for i in range(row + 1):
            self.table_frame.grid_rowconfigure(i, weight=1)

    def open_manage_view(self, table):
        ManageView(self.root, table, self.manager, self)

    def update_chair_stock_label(self):
        self.chair_stock_label.config(text=f"Extra chairs count: {self.manager.chair_stock.get_stock()}")
    
    def view_all_orders(self):
        orders_view = OrdersView(self.root, self.manager.tables)
        orders_view.show_orders()

    def update_table_colors(self):
        self.render_table_view()
        self.root.after(60000, self.update_table_colors)

    def open_reservation_view(self):
        reservation_view = ReservationView(self.root, self.manager)
        reservation_view.show()


