from control import *
#from communication import * Magnuses movement protokol
from decoding import decoder
from filter import fil
from speaker import spk
from microphone import micro
from plotting import plot
from UI import ui


def main():
   
    try:
       for audio_chunk in micro.capture_audio():
           filtered_chunk = fil.butter_bandpass(audio_chunk)
           frequencies, magnitude = fil.analyze_frequency(filtered_chunk)
           
           decoder.process_chunk(frequencies, magnitude)
           
    finally:
        micro.close()
        
        


if __name__ == "__main__":
    #ui.run_example() #UI example code
    main()
    




