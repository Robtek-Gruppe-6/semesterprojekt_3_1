import numpy as np
import sounddevice as sd
from scipy.fft import fft, fftfreq
import time
import pyaudio

global_timeout = 3

# FUNCTIONS
# FUNCTIONS
# FUNCTIONS
# FUNCTIONS
# FUNCTIONS

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
    '*': (941, 1209), # ACK
    '0': (941, 1336),
    '#': (941, 1477), # Hello
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
    print(f"Playing audio: {key}")
    # Play the generated tone
    sd.play(tone, sample_rate)
    sd.wait()  # Wait until the tone finishes playing

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
        (697, 1209): '1', (697, 1336): '2', (697, 1477): '3',
        (770, 1209): '4', (770, 1336): '5', (770, 1477): '6',
        (852, 1209): '7', (852, 1336): '8', (852, 1477): '9',
        (941, 1209): '*', (941, 1336): '0', (941, 1477): '#',
        (697, 1633): 'A', (770, 1633): 'B', (852, 1633): 'C',
        (941, 1633): 'D'
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

# Listen for a specific DTMF tone or timeout and replay if not found
def listen_for_ack(some_DTMF, ack_tone = '*', number_of_attempts = 5):
    rate = 44100
    chunk_size = 1024
    timeout_duration = global_timeout  # Time to wait for "ACK" tone
    counter = 0
    
    while True:
        start_time = time.time()
        acknowledged = False


        print("Listening for ACK tone...")
        for audio_chunk in capture_audio(rate, chunk_size):
            frequencies, magnitude = analyze_frequency(audio_chunk, rate)
            dtmf_tone = identify_dtmf(frequencies, magnitude)

            if dtmf_tone == ack_tone:
                print("ACK received!")
                acknowledged = True
                return True

            # Timeout check
            if time.time() - start_time > timeout_duration:
                print("ACK not received. Retrying...")
                break

            time.sleep(0.01)

        if not acknowledged:
            counter += 1
            if(counter >= number_of_attempts):
                print(f"Didn't receive ACK back in {number_of_attempts} attepmts. Shutting down.")
                return False
            else:
                play_dtmf_tone(some_DTMF)  # Replay DTMF tone



def hello():
    play_dtmf_tone("#") # Wake-up signal
    time.sleep(0.5) 
    bool_received_ack = listen_for_ack("#")
    return bool_received_ack

def movementBlock():
    block = input("Enter a movement block: ")
    block_list = list(block)
    for i in block_list:
        play_dtmf_tone(i)
    return block

# Listen for a specific sequence of DTMF tones
def listen_for_sequence(sequence, max_retries=4):
    rate = 44100
    chunk_size = 1024
    timeout_duration = global_timeout  # Max time to wait for each tone in the sequence

    for attempt in range(max_retries):
        start_time = time.time()
        sequence_index = 0

        print(f"Attempt {attempt + 1} of {max_retries} to detect sequence: {sequence}")
        
        for audio_chunk in capture_audio(rate, chunk_size):
            frequencies, magnitude = analyze_frequency(audio_chunk, rate)
            dtmf_tone = identify_dtmf(frequencies, magnitude)

            # Check for the correct tone in sequence
            if dtmf_tone == sequence[sequence_index]:
                print(f"Detected tone: {dtmf_tone}")
                sequence_index += 1

                # If the entire sequence is detected
                if sequence_index == len(sequence):
                    print("Sequence detected successfully!")
                    return True

            # Check for timeout
            if time.time() - start_time > timeout_duration:
                print("Timeout reached. Restarting sequence detection.")
                break  # Exit current attempt and restart

            # Reset start_time if we detect a tone (keeps waiting time per tone)
            if dtmf_tone:
                start_time = time.time()

            time.sleep(0.01)  # Reduce CPU usage

    print("Failed to detect sequence within retries.")
    return False  # Return false if sequence isn't detected after max_retries

# CODE
# CODE
# CODE
# CODE
# CODE

# SETUP PHASE
print("Welcome to the Robot Movment Block Protocol R.M.B.P.")
print("Enter a movement block after the wake-up-call like this: 2A1*5")

# Main function to play tone and listen for DTMF tones
def main():
    bool_ack = hello() # Send a hello signal and wait for response

    if(bool_ack): # If response is received
        rblock = movementBlock() # Ask user to enter DTMF tones
        listen_for_sequence(rblock)




# Run the main function
if __name__ == "__main__":
    main()
    