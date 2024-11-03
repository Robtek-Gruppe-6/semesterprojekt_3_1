import time #time

from control import *
#from communication import * Magnuses movement protokol
from decoding import decoder
from filter import *
from speaker import *
from microphone import *
from plotting import *


def receiver():
    rate = 44100  # Sample rate
    chunk_size = 1024  # Audio chunk size #With this sample rate and audio chuck size we measure every 23.2 milliseconds (Chuncksize/Samplerate = time per chunck)
    cutoff = 650 #High pass cutoff frequency (slighlty lower than the lowest dtmf tone)
    stopoff = 1800 #Stopoff for bandpass
    last_detected = None
    debounce_time = 0.5  # seconds default 0.5 seconds
    #Future maybe do more readings then sending and then average out before giving output
    

    for audio_chunk in capture_audio(rate, chunk_size):
        #Apply band pass butterworth filter
        filtered_chunk = butter_bandpass(audio_chunk, cutoff, stopoff, rate)

        #Apply high pass butter worth filter
        #filtered_chunk = butter_highpass(audio_chunk, cutoff, rate)

        #Analyze frequencies
    
        frequencies, magnitude = analyze_frequency(filtered_chunk, rate) #Filtered chunck her for brug af filter og audio_chunck hvis uden filter

        #Only used for debugging
        raw_frequencies, raw_magnitude = analyze_frequency(audio_chunk, rate)

        #Identify DTMF tone
        dtmf_tone = decoder.identify_dtmf(frequencies, magnitude)

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




