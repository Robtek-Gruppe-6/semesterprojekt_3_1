from control import *
from decoding import decoder
from filter import fil
from speaker import spk
from microphone import micro
from plotting import plot
from UI import ui
from datalink import datalinker
from dataframer import framer
from transport import flowcontrol



def main():
    start_byte = False
    counter = 0
    len1_bool = False
    len2_bool = False
    crc1_bool = False
    crc2_bool = False
    counting_done = False
    data = []
    length_val = 255
    
    #Transmitter side
    data = ui.ui()
    frame = framer.build_frame(data)
    print(f"Frame: {frame}")
    spk.play_list_of_tones(frame)
    
    
#    framer.input_binary()
#
#    try:
#        for audio_chunk in micro.capture_audio():
#            filtered_chunk = fil.butter_bandpass(audio_chunk)
#            frequencies, magnitude = fil.analyze_frequency(filtered_chunk)
#
#            
#            binary_val = decoder.process_chunk(frequencies, magnitude)
#            #binary_val = int(input("input: "))
#            flowcontrol.reciver_flowcontrol(binary_val)
#            
#                    
#
#            
#            
#            
#                
#           
#           #if binary_val is not None:
#           #    result = datalinker.receive_data(binary_val)
#           #    if result:
#           #         
#           #         collected_data, data_length = result
#           #         print("Collected Data:", [bin(int(b, 2))[2:].zfill(4) for b in collected_data])
#           #         print("Data Length:", data_length)
#           
#           
#           
#    finally:
#        micro.close()
#        
        


if __name__ == "__main__":
    main()
    




