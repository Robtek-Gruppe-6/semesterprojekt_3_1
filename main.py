from control import *
from protocolClass import proto 
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
           #bool_ack = proto.hello()
           #proto.movementBlock(bool_ack)
           
    finally:
        micro.close()
        
        


if __name__ == "__main__":
    #ui.run_example() #UI example code
    #ui.run_protocol() #Runs the movementProtocol but it needs to display that into the UI SO NOT DONE!
    main()
    




