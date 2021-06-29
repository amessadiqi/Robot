from deepspeech import Model


class ASR:
    def __init__(self):
        self.ds = Model('/home/amine/Desktop/Robot/senses/hearing/asr/deepspeech-0.9.3-models.pbmm')
        self.desired_sample_rate = self.ds.sampleRate()

    def stt(self, audio, sr):
        if self.desired_sample_rate == sr:
            return self.ds.stt(audio)
