from scipy.signal import butter, lfilter, freqz, filtfilt #butterworth filter
from scipy.fft import fft, fftfreq #Fast Fourirer transfrom
import numpy as np

class Filter:
    def __init__(self, order = 6): #Default order is set to 6
        # Default filter order can be overridden
        self.order = order

    #Bandpass filter using Butterworth design
    def butter_bandpass(self, data, cutoff, stopoff, fs): 
        nyquist = 0.5 * fs
        high = stopoff / nyquist
        low = cutoff / nyquist
        b, a = butter(self.order,[low, high], btype='bandpass')
        filtered_data = lfilter(b,a,data)
        return filtered_data

    #Butterworth Highpass filter 
    #def butter_highpass(data, cutoff, fs, order = 2): #2nd order?
    #    nyquist = 0.5 * fs
    #    high = cutoff / nyquist
    #    b, a = butter(order, high, btype='highpass', analog=False)
    #    filtered_data = lfilter(b,a,data)
    #    return filtered_data


    #Frequency analysis using FFT
    @staticmethod
    def analyze_frequency(data, rate):
        window = np.hamming(len(data))
        data_windowed = data * window
        N = len(data_windowed)
        yf = fft(data_windowed)
        xf = fftfreq(N, 1 / rate)

        positive_frequencies = xf[:N // 2]
        magnitude = np.abs(yf[:N // 2])

        return positive_frequencies, magnitude
    
fil = Filter() #Laver instans til main