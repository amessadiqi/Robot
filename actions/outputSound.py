import pyaudio
from threading import Thread
from time import sleep


class speaker:
    def __init__(self, st_mem, channels, rate):
        self.st_mem = st_mem
        
        format = pyaudio.paInt16
        audio = pyaudio.PyAudio()
        self.stream = audio.open(format=format, channels=channels,
                rate=rate, output=True)

    def speak(self):
        while True:
            data = self.st_mem.get('hearing')
            print(data['data'])

            soundOutputThread = Thread(target=self.output, args=(data,))
            soundOutputThread.start()

            sleep(1)

    def launch(self):
        speakerThread = Thread(target=self.speak, args=())
        speakerThread.start()

    def output(self, data):
        audioData = data['data']
        self.stream.write(audioData)
