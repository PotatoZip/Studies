import tkinter as tk

class OrdersView:
    def __init__(self, root, tables):
        self.tables = tables
        self.root = root

    def show_orders(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("Orders")
        self.window.geometry("300x600")

        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(main_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = tk.Text(main_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=text_widget.yview)

        text_widget.tag_configure("bold", font=("Arial", 12, "bold"))

        for table in self.tables:
            text_widget.insert(tk.END, f"Table {table.id}:\n", "bold")
            if table.note:
                text_widget.insert(tk.END, f"{table.note}\n\n")
            else:
                text_widget.insert(tk.END, "No orders for this table.\n\n")

        text_widget.config(state=tk.DISABLED)
