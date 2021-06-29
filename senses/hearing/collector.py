import pyaudio
import time
import numpy as np
from array import array


class Collector:
    def __init__(self, rate=16000):
        self.audio = pyaudio.PyAudio()
        self.device = 0
        self.chunk = 0
        self.stream = None
        self.threshold = 0

        self.rate = rate

    def init_stream(self, format=pyaudio.paInt16, channels=1, chunk=128):
        if self.device == 0:
            print("Error - Select input device first before initializing stream.")
        else:
            self.chunk = chunk
            self.stream = self.audio.open(format=format, channels=channels,
                rate=self.rate, input=True,
                frames_per_buffer=chunk,
                input_device_index=self.device)

            print("Stream initialized with configuration:")
            print("\tFormat :", format)
            print("\tChannels :", channels)
            print("\tSample rate :", self.rate)
            print("\tChunk :", chunk)

    def device_selection(self):
        info = self.audio.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        available_devices_ids = []
        for i in range(0, numdevices):
            if (self.audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print ("Input Device id ", i, " - ", self.audio.get_device_info_by_host_api_device_index(0, i).get('name'))
                available_devices_ids.append(i)

        while self.device == 0:
            device = int(input("Enter device id: "))

            if device in available_devices_ids:
                self.device = device

            if self.device == 0:
                print("Input device with id", device, "doesn't exist")
            else:
                print("Input device selected: ", self.audio.get_device_info_by_host_api_device_index(0, device).get('name'))

    def threshold_selection(self):
        while self.threshold <= 0:
            self.threshold = float(input("Enter choosen microphone threshold : "))

    def listen(self):
        if self.device == 0:
            self.device_selection()

        if self.stream is None:
            self.init_stream()

        if self.threshold == 0:
            self.threshold_selection()

        wav_data = []
        detected = False

        while True:
            data = self.stream.read(self.chunk, exception_on_overflow = False)
            value = max(array('h', data))
            
            if value > self.threshold:
                detected_time = time.time()
                while time.time() - detected_time < 5:
                    wav_data.append(np.frombuffer(data, dtype='int16'))

                    data = self.stream.read(self.chunk, exception_on_overflow = False)
                    value = max(array('h', data))
                    detected = True

            if detected:
                return np.array(wav_data).flatten()

    def terminate(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
