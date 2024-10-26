import numpy as np
import sounddevice as sd

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

# Sampling parameters
sample_rate = 44100  # Standard audio sample rate (44.1 kHz)
duration = 0.5       # Tone duration in seconds

# Function to generate DTMF tone for a key
def generate_dtmf_tone(key, duration=0.5, sample_rate=44100):
    if key not in dtmf_frequencies:
        raise ValueError(f"Invalid DTMF key: {key}")

    low_freq, high_freq = dtmf_frequencies[key]
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # Generate the two sine waves and sum them to create the DTMF tone
    tone = (np.sin(2 * np.pi * low_freq * t) + np.sin(2 * np.pi * high_freq * t)) * 0.5
    
    return tone

# Function to play the DTMF tone
def play_dtmf_tone(key):
    tone = generate_dtmf_tone(key, duration, sample_rate)
    
    # Play the generated tone
    sd.play(tone, sample_rate)
    sd.wait()  # Wait until the tone finishes playing

# Play DTMF tones here
play_dtmf_tone('A')
play_dtmf_tone('2')
play_dtmf_tone('9')
play_dtmf_tone('7')
play_dtmf_tone('1')
play_dtmf_tone('5')
play_dtmf_tone('0')
play_dtmf_tone('9')
play_dtmf_tone('4')