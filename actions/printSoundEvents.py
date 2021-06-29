from threading import Thread


class printer:
    def __init__(self, st_mem):
        self.st_mem = st_mem

    def printing(self):
        while True:
            data = self.st_mem.get('hearing')

            printingThread = Thread(target=self.print, args=(data,))
            printingThread.start()

    def launch(self):
        printerThread = Thread(target=self.printing, args=())
        printerThread.start()

    def print(self, data):
        print(data["type"])
        if 'Speech' in data['type']:
            if not data['class'] is None:
                print("\tYou said:", data['class'])
            else:
                print("Can't understand the speech")
        print("")
