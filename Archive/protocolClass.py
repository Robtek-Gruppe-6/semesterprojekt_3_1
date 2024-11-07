from decoding import decoder
from speaker import spk
from microphone import micro
import numpy as np
import sounddevice as sd
from scipy.fft import fft, fftfreq
import time
import pyaudio
from filter import fil


class MovementProtocol:

    def __init__(self, sample_rate = 44100, chunk_size = 1024, timeout_duration = 5, duration = 0.5):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.timeout_duration = timeout_duration
        self.duration = duration

        self.dtmf_freqs = {
            (697, 1209): '1', (697, 1336): '2', (697, 1477): '3', (697, 1633): 'A',
            (770, 1209): '4', (770, 1336): '5', (770, 1477): '6', (770, 1633): 'B',
            (852, 1209): '7', (852, 1336): '8', (852, 1477): '9', (852, 1633): 'C',
            (941, 1209): '*', (941, 1336): '0', (941, 1477): '#', (941, 1633): 'D',
        }

    def listen_for_ack(self, some_DTMF, ack_tone = '*', number_of_attempts = 5):
        counter = 0
        
        while True:
            start_time = time.time()
            acknowledged = False


            print("Listening for ACK tone...")
            for audio_chunk in micro.capture_audio():
                frequencies, magnitude = fil.analyze_frequency(audio_chunk)
                dtmf_tone = decoder.identify_dtmf(frequencies, magnitude)

                if dtmf_tone == ack_tone:
                    print("ACK received!")
                    acknowledged = True
                    return True

                # Timeout check
                if time.time() - start_time > self.timeout_duration:
                    print("ACK not received. Retrying...")
                    break

                time.sleep(0.01)

            if not acknowledged:
                counter += 1
                if(counter >= number_of_attempts):
                    print(f"Didn't receive ACK back in {number_of_attempts} attepmts. Shutting down.")
                    return False
                else:
                    spk.play_dtmf_tone(some_DTMF)  # Replay DTMF tone



    def hello(self):
        spk.play_dtmf_tone("#") # Wake-up signal
        time.sleep(0.5) 
        bool_received_ack = self.listen_for_ack("#")
        return bool_received_ack

    def movementBlock(self):
        block = input("Enter a movement block: ")
        block_list = list(block)
        for i in block_list:
            spk.play_dtmf_tone(i)
        return block

    # Listen for a specific sequence of DTMF tones
    def listen_for_sequence(self, sequence, max_retries=4):

        for attempt in range(max_retries):
            start_time = time.time()
            sequence_index = 0

            print(f"Attempt {attempt + 1} of {max_retries} to detect sequence: {sequence}")
            
            for audio_chunk in micro.capture_audio():
                frequencies, magnitude = fil.analyze_frequency(audio_chunk)
                dtmf_tone = decoder.identify_dtmf(frequencies, magnitude)

                # Check for the correct tone in sequence
                if dtmf_tone == sequence[sequence_index]:
                    print(f"Detected tone: {dtmf_tone}")
                    sequence_index += 1

                    # If the entire sequence is detected
                    if sequence_index == len(sequence):
                        print("Sequence detected successfully!")
                        return True

                # Check for timeout
                if time.time() - start_time > self.timeout_duration:
                    print("Timeout reached. Restarting sequence detection.")
                    break  # Exit current attempt and restart

                # Reset start_time if we detect a tone (keeps waiting time per tone)
                if dtmf_tone:
                    start_time = time.time()

                time.sleep(0.01)  # Reduce CPU usage

        print("Failed to detect sequence within retries.")
        return False  # Return false if sequence isn't detected after max_retries


    def repeat_after_me(self, bool_ack):
        if(bool_ack): # If response is received
            rblock = self.movementBlock() # Ask user to enter DTMF tones
            bool_sqn = self.listen_for_sequence(rblock)
            if(bool_sqn):
                spk.play_dtmf_tone("*")
            else:
                print("Error.")

    def listen_for_hello(self, hello_signal="#"):

        print(f"Waiting for 'hello' signal: {hello_signal}")

        for audio_chunk in micro.capture_audio():
            frequencies, magnitude = fil.analyze_frequency(audio_chunk)
            dtmf_tone = decoder.identify_dtmf(frequencies, magnitude)

            # Check if the detected tone matches the hello signal
            if dtmf_tone == hello_signal:
                print("Hello signal detected!")
                return True

            time.sleep(0.01)  # Reduce CPU usage

proto = MovementProtocol()