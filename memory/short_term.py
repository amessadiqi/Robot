import queue

class ShortTermMemory:
    def __init__(self):
        self.hearing = queue.Queue()

    def put(self, sense, data):
        if sense == 'hearing':
            self.hearing.put(data)

    def get(self, sense):
        if sense == 'hearing':
            return self.hearing.get()
