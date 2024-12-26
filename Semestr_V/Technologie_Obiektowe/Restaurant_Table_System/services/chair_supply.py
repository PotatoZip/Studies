class ChairSupply:
    def __init__(self, initial_stock):
        self.stock = initial_stock

    def take_chairs(self, amount):
        if amount > self.stock:
            raise ValueError("Brak wystarczającej liczby krzesełek w magazynie!")
        self.stock -= amount
        return amount

    def return_chairs(self, amount):
        self.stock += amount

    def get_stock(self):
        return self.stock