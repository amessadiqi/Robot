import queue

class LinguisticMemory:
    def __init__(self):
        self.speech = queue.Queue()

    def put(self, sentence):
        self.speech.put(sentence)

    def get(self):
        return self.speech.get()
