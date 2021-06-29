import speech_recognition as sr

class ASR:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def stt(self, audio, sr):
        audio_bytes = audio.tobytes()
        audio_source = sr.AudioFile(audio_bytes, sr, 1)
        
        audioData = self.recognizer.record(audio_source)

        return self.recognizer.recognize_google(audioData)
