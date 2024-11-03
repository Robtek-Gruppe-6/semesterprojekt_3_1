import numpy as np
from scipy.signal import butter, lfilter, freqz, filtfilt #butterworth filter

import matplotlib.pyplot as plt #Plotting

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