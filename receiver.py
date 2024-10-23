import pyaudio
import numpy as np
from scipy.fft import fft, fftfreq
import time

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

def analyze_frequency(data, rate):
    window = np.hamming(len(data))
    data_windowed = data * window
    N = len(data_windowed)
    yf = fft(data_windowed)
    xf = fftfreq(N, 1 / rate)

    positive_frequencies = xf[:N // 2]
    magnitude = np.abs(yf[:N // 2])

    return positive_frequencies, magnitude

def identify_dtmf(frequencies, magnitude):
    dtmf_freqs = {
        (697, 1209): '1', (697, 1336): '2', (697, 1477): '3', (697, 1633): 'A',
        (770, 1209): '4', (770, 1336): '5', (770, 1477): '6', (770, 1633): 'B',
        (852, 1209): '7', (852, 1336): '8', (852, 1477): '9', (852, 1633): 'C',
        (941, 1209): '*', (941, 1336): '0', (941, 1477): '#', (941, 1633): 'D',
    }

    # Find the two highest magnitudes
    top_indices = np.argsort(magnitude)[-2:]
    detected_frequencies = frequencies[top_indices]

    # Identify the closest DTMF frequencies
    low_detected = min(detected_frequencies)
    high_detected = max(detected_frequencies)
    for (low_freq, high_freq), digit in dtmf_freqs.items():
        if (abs(low_detected - low_freq) < 20) and (abs(high_detected - high_freq) < 20):
            return digit
    return None

def receiver():
    rate = 44100  # Sample rate
    chunk_size = 1024  # Audio chunk size
    last_detected = None
    debounce_time = 0.5  # seconds

    for audio_chunk in capture_audio(rate, chunk_size):
        frequencies, magnitude = analyze_frequency(audio_chunk, rate)
        dtmf_tone = identify_dtmf(frequencies, magnitude)

        if dtmf_tone and dtmf_tone != last_detected:
            print(f"Detected DTMF Tone: {dtmf_tone}")
            last_detected = dtmf_tone
            last_time = time.time()
        elif last_detected and (time.time() - last_time) > debounce_time:
            last_detected = None

        time.sleep(0.01)  # Sleep to reduce CPU usage

if __name__ == "__main__":
    receiver()