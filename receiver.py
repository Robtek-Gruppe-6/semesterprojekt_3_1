import pyaudio #to Capture audio
import numpy as np
from scipy.fft import fft, fftfreq #Fast Fourirer transfrom
from scipy.signal import butter, lfilter, freqz, filtfilt #butterworth filter
import time #time
import matplotlib.pyplot as plt #Plotting

#Plotting
#Plotting frequency domain
def plot_frequency_domain(frequencies, magnitude):
    plt.figure()
    plt.plot(frequencies, magnitude)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.title('Frequency Domain Representation of Audio Data')
    plt.xlim([0, 2000])
    plt.show()
#Plotting filter response
def plot_filter_response(cutoff, fs, order=4):
    nyquist = 0.5 * fs
    high = cutoff / nyquist
    b, a = butter(order, high, btype='high')

    w, h = freqz(b, a, worN=8000)
    plt.plot(0.5 * fs * w / np.pi, np.abs(h), 'b')
    plt.plot(cutoff, 0.5 * np.sqrt(2), 'ro')
    plt.title('Highpass Filter Frequency Response')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain')
    plt.grid()
    plt.xlim(0, 2000)
    plt.show()
    
#Plotting end


#Butterworth Highpass filter 
def butter_highpass(data, cutoff, fs, order = 2): #8th order
    nyquist = 0.5 * fs
    high = cutoff / nyquist
    b, a = butter(order, high, btype='highpass', analog=False)
    filtered_data = lfilter(b,a,data)
    return filtered_data

#def apply_highpass_filter(data, cutoff, fs, order = 8): #8th order
#    b, a = butter_highpass(cutoff, fs, order=order)
#    filtered_data = lfilter(b, a, data)
#    return filtered_data


#Function to capture audio using PyAudio that uses PortAudio
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

    magnitude_threshold = 50000 #Threshold to not detect noise

    #Find the two highest mangittudes that exceed the threshold
    filtered_indices = [i for i in range(len(magnitude)) if magnitude[i] > magnitude_threshold]

    #If we have at least two valid indicies, continue

    if len(filtered_indices) >= 2:
        top_indices = np.argsort(magnitude[filtered_indices])[-2:] #Get the indices of the top two magnitudes
        detected_frequencies = frequencies[filtered_indices][top_indices]

        # Idemtify the closest DTMF frequencies
        low_detected = min(detected_frequencies)
        high_detected = max(detected_frequencies)
        for (low_freq, high_freq), digit in dtmf_freqs.items():
            if (abs(low_detected - low_freq) < 20) and (abs(high_detected - high_freq) < 20):
                return digit
    return None

def receiver():
    rate = 44100  # Sample rate
    chunk_size = 1024  # Audio chunk size #With this sample rate and audio chuck size we measure every 23.2 milliseconds (Chuncksize/Samplerate = time per chunck)
    cutoff = 675 #High pass cutoff frequency (slighlty lower than the lowest dtmf tone)
    last_detected = None
    debounce_time = 0.5  # seconds default 0.5 seconds
    #Future maybe do more readings then sending and then average out before giving output

    for audio_chunk in capture_audio(rate, chunk_size):
        #Apply high pass butter worth filter
        filtered_chunk = butter_highpass(audio_chunk, cutoff, rate)

        #Analyze frequencies
    
        frequencies, magnitude = analyze_frequency(filtered_chunk, rate) #Filtered chunck her for brug af filter og audio_chunck hvis uden filter

        #Only used for debugging
        raw_frequencies, raw_magnitude = analyze_frequency(audio_chunk, rate)

        #Identify DTMF tone
        dtmf_tone = identify_dtmf(frequencies, magnitude)

        if dtmf_tone and dtmf_tone != last_detected:
            print(f"Detected DTMF Tone: {dtmf_tone}")
            last_detected = dtmf_tone
            last_time = time.time()

            #Plot the frequency domain after a tone
            #ONLY USE FOR DEBUG
            #plot_frequency_domain(raw_frequencies, raw_magnitude)
            #plot_frequency_domain(frequencies, magnitude)
            #plot_filter_response(cutoff, rate)

        elif last_detected and (time.time() - last_time) > debounce_time:
            last_detected = None

        time.sleep(0.01)  # Sleep to reduce CPU usage

if __name__ == "__main__":
    receiver()