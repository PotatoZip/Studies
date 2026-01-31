from currency import Currency
from currencyCollection import CurrencyCollection

class Exchanger():

    def __init__(self, currencyCollection):
        self.currencyCollection = currencyCollection

    def exchange(self, firstCurrency: Currency, secondCurrency: Currency, amount) -> float:
        if amount < 0:
            raise ValueError("Amount must be greater than zero.")
        
        fromCurrency = next((c for c in self.currencyCollection.getCurrencies() if c.getCode() == firstCurrency), None)
        toCurrency = next((c for c in self.currencyCollection.getCurrencies() if c.getCode() == secondCurrency), None)
        
        return (amount * fromCurrency.getRate()) / toCurrency.getRate()
    
    def getInstance(self):
        return Exchanger()
        