import numpy as np
import sounddevice as sd

class Speaker:
    #Class variables
    # Sampling parameters
    sample_rate = 44100  # Standard audio sample rate (44.1 kHz)
    duration = 0.5       # Tone duration in seconds Defualt = 0.5

    # DTMF Frequencies (low and high)
    dtmf_frequencies = {
        '1': (697, 1209),
        '2': (697, 1336),
        '3': (697, 1477),
        '4': (770, 1209),
        '5': (770, 1336),
        '6': (770, 1477),
        '7': (852, 1209),
        '8': (852, 1336),
        '9': (852, 1477),
        '*': (941, 1209),
        '0': (941, 1336),
        '#': (941, 1477),
        'A': (697, 1633),
        'B': (770, 1633),
        'C': (852, 1633),
        'D': (941, 1633),
    }

    def __init__(self, duration=None, sample_rate=None):
        #Allow overriding defaults via initilization
        if duration:
            self.duration = duration
        if sample_rate:
            self.sample_rate = sample_rate

    # Function to generate DTMF tone for a key
    def generate_dtmf_tone(self, key):
        if key not in self.dtmf_frequencies:
            raise ValueError(f"Invalid DTMF key: {key}")

        low_freq, high_freq = self.dtmf_frequencies[key]
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), False)

        # Generate the two sine waves and sum them to create the DTMF tone
        tone = (np.sin(2 * np.pi * low_freq * t) + np.sin(2 * np.pi * high_freq * t)) * 0.5
        return tone

    # Function to play the DTMF tone
    def play_dtmf_tone(self, key):
        tone = self.generate_dtmf_tone(key)

        # Play the generated tone
        sd.play(tone, self.sample_rate)
        sd.wait()  # Wait until the tone finishes playing

    def play_all_dtmf_tones(self):
        for key in self.dtmf_frequencies:
            self.play_all_dtmf_tones(key)


    # Play DTMF tones here
    #play_dtmf_tone('A')
    #play_all_dtmf_tones()

spk = Speaker() #Laver instans til main