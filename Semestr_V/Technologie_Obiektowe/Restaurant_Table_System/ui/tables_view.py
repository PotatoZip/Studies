import tkinter as tk
from ui.manage_view import ManageView
from ui.orders_view import OrdersView

class TablesView:
    def __init__(self, manager, root):
        self.manager = manager
        self.root = root

        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        self.chair_stock_label = tk.Label(self.root, text=f"Extra chairs count: {self.manager.chair_stock.get_stock()}")
        self.chair_stock_label.pack(pady=10)

        self.render_table_view()

    def render_table_view(self):
        row = col = 0

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        for table in self.manager.tables:
            button_color = "green" if table.state.__class__.__name__ == "AvailableState" else \
                           "red" if table.state.__class__.__name__ == "OccupiedState" else "yellow"
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
