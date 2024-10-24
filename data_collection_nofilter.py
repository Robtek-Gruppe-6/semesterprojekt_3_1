import pyaudio
import numpy as np
import csv

def capture_audio(rate=44100, chunk_size=1024):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk_size)

    print("Listening for audio data...")

    # Open a CSV file to store the captured audio data
    with open("audio_data.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')  # Ensure commas as delimiters

        try:
            while True:
                try:
                    data = np.frombuffer(stream.read(chunk_size, exception_on_overflow=False), dtype=np.int16)
                    writer.writerow(data)  # Write each chunk as a row in the CSV
                except IOError:
                    # Handle buffer overflow or other I/O errors
                    continue
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()

if __name__ == "__main__":
    capture_audio()
