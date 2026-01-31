from currency import Currency

class CurrencyCollection:

    def __init__(self):
        self.currencies = []

    def addCurrency(self, name, rate, code):
        currency = Currency(name, rate, code)
        self.currencies.append(currency)

    def getCurrencies(self):
        return self.currencies

    def editCurrencies(self, newCurrencies):
        self.currencies = newCurrencies

    def removeCurrency(self):
        pass

    def printCurrencies(self):
        for currency in self.currencies:
            print("Code: " + currency.getCode() + "  Currency: " + currency.getName())