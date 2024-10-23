from abc import ABC, abstractmethod
from currencyCollection import CurrencyCollection
from exchanger import Exchanger
import os

class IUserInterface(ABC):
    @abstractmethod
    def mainLoop(self):
        pass
    
class UserInterface(IUserInterface):

    def __init__(self, currencyCollection):
        self.currencyCollection = currencyCollection

    def mainLoop(self):
        print("-------------------------------\n      Welcome to Exchanger\n-------------------------------\n")
        while(True):
            try:
                tmp = input("Please select:\n1 - Exchange\n2 - Show available currencies\n3 - Exit\n")
                if tmp == "1":
                    os.system('cls')
                    firstCurrency = input("Enter Code of currency you want to exchange:\n")
                    secondCurrency = input("Enter Code of currency you want to receive:\n")
                    amount = input("Enter amount you want to exchange:\n")
                    exchanger = Exchanger(self.currencyCollection)
                    input("\nAmount in new currency: " + str(round(exchanger.exchange(firstCurrency, secondCurrency, float(amount)), 2)) + "\n\nPress any key to continue...")
                    os.system('cls')
                elif tmp == "2":
                    os.system('cls')
                    self.currencyCollection.printCurrencies()
                    input("\nPress any key to continue...")
                    os.system('cls')
                elif tmp == "3":
                    os.system('cls')
                    print("See you")
                    exit()
                else:
                    print("Wrong input")
            except Exception as e:
                    os.system('cls')
                    print(f'Error while exchanging: {e}')
                    input("\nPress any key to continue...")
                    os.system('cls')

