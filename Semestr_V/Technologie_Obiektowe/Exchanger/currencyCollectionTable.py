from currencyCollection import CurrencyCollection

class CurrencyCollectionTable():
    
    def __init__(self, tableName, timestamp):
        self.tableName = tableName
        self.timestamp = timestamp

    def getTableName(self):
        return self.tableName
    
    def setTableName(self, tableName):
        self.tableName = tableName

    def getTimestamp(self):
        return self.timestamp
    
    def setTimestamp(self, timestamp):
        self.timestamp = timestamp
