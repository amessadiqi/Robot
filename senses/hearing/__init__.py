import speech_recognition as sr
from threading import Thread

from .collector import Collector
from .sec import SEC
from .asr import ASR


class Hearing:
    def __init__(self, st_mem, rate=16000):
        self.memory = st_mem

        self.rate = rate

        self.collector = Collector(rate=self.rate)
        self.sec = SEC()
        self.asr = ASR()

    def launch(self):
        hearingThread = Thread(target=self.hear, args=())
        hearingThread.start()

    def hear(self):
        while True:
            audio = self.collector.listen()

            processingThread = Thread(target=self.process, args=(audio,))
            processingThread.start()

    def process(self, audio):
        # Noise reduction

        soundEvents = self.sec.classify(wav_data=audio, sr=self.rate)

        # Audio source separation

        data = {"type":soundEvents}

        if 'Speech' in soundEvents:
            data["data"] = audio
            """data["class"] = self.asr.stt(audio=audio, sr=16000)"""

            r = sr.Recognizer()
            audioData = sr.AudioData(frame_data=audio, sample_rate=self.rate, sample_width=2)
            
            try:
                data["class"] = r.recognize_google(audioData)
            except:
                data["class"] = None
        else:
            data["data"] = audio
        
        stmemThread = Thread(target=self.store, args=(data, ))
        stmemThread.start()

    def store(self, data):
        self.memory.put('hearing', data)

    def terminate(self):
        if not self.mic is None:
            self.mic.terminate()
