import numpy as np
from filter import fil
from plotting import plot
import time #time

class Decoding:
    def __init__(self, debounce_time = 0.5, magnitude_threshold = 100000, frequency_tolerance = 20, last_detected = None, last_time = None):
        # Define DTMF frequency pairs with their corresponding digits
        self.dtmf_freqs = {
            (697, 1209): '1', (697, 1336): '2', (697, 1477): '3', (697, 1633): 'A',
            (770, 1209): '4', (770, 1336): '5', (770, 1477): '6', (770, 1633): 'B',
            (852, 1209): '7', (852, 1336): '8', (852, 1477): '9', (852, 1633): 'C',
            (941, 1209): '*', (941, 1336): '0', (941, 1477): '#', (941, 1633): 'D',
        }
        self.magnitude_threshold = magnitude_threshold  # Minimum magnitude to avoid noise detection
        self.frequency_tolerance = frequency_tolerance  # Allowed tolerance for frequency matching
        self.fil = fil
        self.debounce_time = debounce_time
        self.last_detected = last_detected
        self.last_time = last_time


        
    def identify_dtmf(self, frequencies, magnitude):
        
        #Find the two highest mangittudes that exceed the threshold
        filtered_indices = [i for i in range(len(magnitude)) if magnitude[i] > self.magnitude_threshold]

        #If we have at least two valid indicies, continue
        if len(filtered_indices) >= 2:
            top_indices = np.argsort(magnitude[filtered_indices])[-2:] #Get the indices of the top two magnitudes
            detected_frequencies = frequencies[filtered_indices][top_indices]

            # Idemtify the closest DTMF frequencies
            low_detected = min(detected_frequencies)
            high_detected = max(detected_frequencies)
            for (low_freq, high_freq), digit in self.dtmf_freqs.items():
                if (abs(low_detected - low_freq) < self.frequency_tolerance) and (abs(high_detected - high_freq) < self.frequency_tolerance):
                    return digit
        return None
    
    def process_chunk(self, frequencies, magnitude):
        
            #Apply band pass butterworth filter
            #filtered_chunk = fil.butter_bandpass(audio_chunk)

            #Analyze frequencies
            #frequencies, magnitude = fil.analyze_frequency(filtered_chunk) #Filtered chunck her for brug af filter og audio_chunck hvis uden filter

            #Only used for debugging
            #raw_frequencies, raw_magnitude = fil.analyze_frequency(audio_chunk, fil.rate)

            #Identify DTMF tone
            dtmf_tone = self.identify_dtmf(frequencies, magnitude)

            if dtmf_tone and dtmf_tone != self.last_detected:
                print(f"Detected DTMF Tone: {dtmf_tone}") #Det her kunne godt tænkes at være i application layer, da de jo printer til UI
                self.last_detected = dtmf_tone
                self.last_time = time.time()

                #Plot the frequency domain after a tone
                #ONLY USE FOR DEBUG
                #plot_frequency_domain(raw_frequencies, raw_magnitude)
                plot.frequency_domain(frequencies, magnitude)
                #plot_filter_response(cutoff, rate)

            elif self.last_detected and (time.time() - self.last_time) > self.debounce_time:
                self.last_detected = None

            time.sleep(0.01)  # Sleep to reduce CPU usage
      
decoder = Decoding() #Laver instans til main