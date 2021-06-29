from threading import Thread

from .stcls import SentenceClassifier


class MainProcessor:
    def __init__(self, st_mem, ling_mem):
        self.st_mem = st_mem
        self.ling_mem = ling_mem

        self.sentenceClassifier = SentenceClassifier()

    def launch(self):
        mainProcessorThread = Thread(target=self.process, args=())
        mainProcessorThread.start()

    def process(self):
        while True:
            data = self.st_mem.get('hearing')

            print(data["type"])
            if 'Speech' in data['type']:
                if not data['class'] is None:
                    print("\tYou said:", data['class'])

                    # Classify sentence type
                    sentenceType = self.sentenceClassifier.classify(data['class'])
                    print("\t\tType -> ", sentenceType)

                    # Classify intent
                else:
                    print("Can't understand the speech")
            print("")

    def classifySentence(self, sentence):
        pass

    def predictIntent(self):
        pass
