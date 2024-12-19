import pyaudio #to Capture audio
import numpy as np


class Microphone:
    def __init__(self, rate = 44100, chunk_size = 1024):
        self.data = None
        self.rate = rate #Sample rate
        self.chunk_size = chunk_size #Audio chunk size #With this sample rate and audio chuck size we measure every 23.2 milliseconds (Chuncksize/Samplerate = time per chunck)
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=self.rate,
                            input=True,
                            frames_per_buffer=self.chunk_size)
    
    def capture_audio(self):
        print("Listening for DTMF tones...")
        try:
            while True:
                try:
                    self.data = np.frombuffer(self.stream.read(self.chunk_size, exception_on_overflow=False), dtype=np.int16)
                    yield self.data
                except IOError:
                    continue
        finally:
            self.close()
            
            
    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        
    
micro = Microphone()