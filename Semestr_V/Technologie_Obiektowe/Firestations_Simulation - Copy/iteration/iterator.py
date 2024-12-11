class Iterator:
    def __init__(self, stations):
        self.stations = stations
        self.index = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.stations):
            station = self.stations[self.index]
            self.index += 1
            return station
        else:
            raise StopIteration