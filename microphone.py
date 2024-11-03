import pyaudio #to Capture audio
import numpy as np

def capture_audio(rate=44100, chunk_size=1024):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk_size)

    print("Listening for DTMF tones...")
    try:
        while True:
            try:
                data = np.frombuffer(stream.read(chunk_size, exception_on_overflow=False), dtype=np.int16)
                yield data
                #print(data) #Tester hvad vi får
            except IOError:
                # Handle buffer overflow or other I/O errors
                continue
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()