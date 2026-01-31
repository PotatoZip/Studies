class Currency():
    name = str
    rate = float
    code = str

    def __init__(self, name, rate, code):
        self.name = name
        self.rate = rate
        self.code = code

    def getName(self) -> str:
        return self.name
    
    def setName(self, name):
        self.name = name

    def getRate(self) -> float:
        return self.rate
    
    def setRate(self, rate):
        self.rate = rate

    def getCode(self) -> float:
        return self.code
    
    def setCode(self, code):
        self.code = code

    def isEqual(self, sampleCode) -> bool:
        if self.code == sampleCode:
            return True
        else:
            return False