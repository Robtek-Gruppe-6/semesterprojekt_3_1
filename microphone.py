import pyaudio #to Capture audio
import numpy as np


class Microphone:
    def __init__(self, rate = 44100, chunk_size = 1024):
        self.rate = rate #Sample rate
        self.chunk_size = chunk_size #Audio chunk size #With this sample rate and audio chuck size we measure every 23.2 milliseconds (Chuncksize/Samplerate = time per chunck)

    
    def capture_audio(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=self.rate,
                            input=True,
                            frames_per_buffer=self.chunk_size)

        print("Listening for DTMF tones...")
        try:
            while True:
                try:
                    data = np.frombuffer(stream.read(self.chunk_size, exception_on_overflow=False), dtype=np.int16)
                    yield data
                    #print(data) #Tester hvad vi får
                except IOError:
                    # Handle buffer overflow or other I/O errors
                    continue
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
micro = Microphone()