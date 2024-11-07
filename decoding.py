import numpy as np
from filter import fil
from plotting import plot
import time #time

class Decoding:
    def __init__(self, debounce_time = 0.5, magnitude_threshold = 100000, frequency_tolerance = 10, last_detected = None, last_time = None):
        # Define DTMF frequency pairs with their corresponding digits
        self.dtmf_freqs = {
            (697, 1209): ('1', 0b0001), (697, 1336): ('2', 0b0010), (697, 1477): ('3', 0b0011), (697, 1633): ('A', 0b1010),
            (770, 1209): ('4', 0b0100), (770, 1336): ('5', 0b0101), (770, 1477): ('6', 0b0110), (770, 1633): ('B', 0b1011),
            (852, 1209): ('7', 0b0111), (852, 1336): ('8', 0b1000), (852, 1477): ('9', 0b1001), (852, 1633): ('C', 0b1100),
            (941, 1209): ('E', 0b1110), (941, 1336): ('0', 0b0000), (941, 1477): ('F', 0b1111), (941, 1633): ('D', 0b1101),
        } # = F and * = E
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

            # Identify the closest DTMF frequencies
            low_detected = min(detected_frequencies)
            high_detected = max(detected_frequencies)
            for (low_freq, high_freq), (digit, binary_val) in self.dtmf_freqs.items():
                if (abs(low_detected - low_freq) < self.frequency_tolerance) and (abs(high_detected - high_freq) < self.frequency_tolerance):
                    return digit, binary_val
        return None, None
    
    def process_chunk(self, frequencies, magnitude):

            #Identify DTMF tone
            dtmf_tone, binary_value = self.identify_dtmf(frequencies, magnitude)

            if dtmf_tone and dtmf_tone != self.last_detected:
                print(f"Detected DTMF Tone: {dtmf_tone}") #Det her kunne godt tænkes at være i application layer, da de jo printer til UI
                self.last_detected = dtmf_tone
                self.last_time = time.time()
                
                return binary_value

                #Plot the frequency domain after a tone
                #ONLY USE FOR DEBUG
                #plot_frequency_domain(raw_frequencies, raw_magnitude)
                #plot.frequency_domain(frequencies, magnitude)
                #plot_filter_response(cutoff, rate)

            elif self.last_detected and (time.time() - self.last_time) > self.debounce_time:
                self.last_detected = None

            time.sleep(0.01)  # Sleep to reduce CPU usage
            return None
        
           
            

decoder = Decoding() #Laver instans til main