class Iterator:
    def __init__(self, events):
        self.events = events
        self.index = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.events):
            event = self.events[self.index]
            self.index += 1
            return event
        else:
            raise StopIteration