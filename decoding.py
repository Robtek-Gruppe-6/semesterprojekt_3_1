import numpy as np

class Decoding:
    def __init__(self, magnitude_threshold=50000, frequency_tolerance=20):
        # Define DTMF frequency pairs with their corresponding digits
        self.dtmf_freqs = {
            (697, 1209): '1', (697, 1336): '2', (697, 1477): '3', (697, 1633): 'A',
            (770, 1209): '4', (770, 1336): '5', (770, 1477): '6', (770, 1633): 'B',
            (852, 1209): '7', (852, 1336): '8', (852, 1477): '9', (852, 1633): 'C',
            (941, 1209): '*', (941, 1336): '0', (941, 1477): '#', (941, 1633): 'D',
        }
        self.magnitude_threshold = magnitude_threshold  # Minimum magnitude to avoid noise detection
        self.frequency_tolerance = frequency_tolerance  # Allowed tolerance for frequency matching


        
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
    
decoder = Decoding() #Laver instans til main