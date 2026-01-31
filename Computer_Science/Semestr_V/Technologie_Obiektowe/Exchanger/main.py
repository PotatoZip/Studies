from userInterface import UserInterface
from dataParser import DataParser
from dataProvider import DataProvider
from currencyCollection import CurrencyCollection

def run():
    dataProvider = DataProvider()
    currencies = CurrencyCollection()
    parser = DataParser(dataProvider.getData())
    parser.parseData(currencies)
    userInterface = UserInterface(currencies)
    userInterface.mainLoop()

if __name__ == "__main__":
    run()