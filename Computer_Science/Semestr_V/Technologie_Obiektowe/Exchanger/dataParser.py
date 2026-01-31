class DataParser():

    def __init__(self, toParse):
        self.toParse = toParse

    def parseData(self, currencyCollection):
        if self.toParse is None:
            print("No data to parse")
            return
        try:
            for item in self.toParse[0]['rates']: 
                currency = item['currency']
                code = item['code']
                mid = item['mid']
                currencyCollection.addCurrency(currency, mid, code)
            currencyCollection.addCurrency("Zloty", 1, "PLN")
        except Exception as e:
            print(f'Error while preparing JSON: {e}')
        
    