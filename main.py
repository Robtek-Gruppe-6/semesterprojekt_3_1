#from control import *
from decoding import decoder
from filter import fil
from speaker import spk
from microphone import Microphone
from datalink import datareceiver
from transport import flowcontrol
from robotcommandlayer import PresentationLayer
#from plotting import plot
from UI import ui
#from datalink import datalinker
from dataframer import framer
import threading
import time
#from mqtt_pub import publish_command, start_mqtt, stop_mqtt #Importing the neccecary functions from mqtt_pub.py

#COMPUTER
def listening_stack():
    start_time = time.time()
    
    micro = Microphone()
    
    try:
        data_rec = None
        
        for audio_chunk in micro.capture_audio():
            if time.time() - start_time > 5:
                print("Timeout reached, exiting listening stack...")
                return False, None
            filtered_chunk = fil.butter_bandpass(audio_chunk)
            frequencies, magnitude = fil.analyze_frequency(filtered_chunk)
            binary_val = decoder.process_chunk(frequencies, magnitude)
            crc, _, _, datasegment = datareceiver.frame_receiver(binary_val)
            data_rec = flowcontrol.computer_receiver_flowcontrol(crc, datasegment)

            if data_rec is not None:
                break
        return True, data_rec
    finally:
        micro.close()
        

def main():
    
    #Transmitter side
    while True:
        flow_bool = False
        loop_exit = ui.interface()
        data = ui.datalist
        segment = flowcontrol.transmitter_add_label(data)
        frame = framer.build_frame(segment)
        print(f"Frame: {frame}")
        while(not flow_bool):
            spk.play_list_of_tones(frame)
            flow_bool, data_rec = listening_stack()
            print(flow_bool)
        
       
        
        ui.datalist = []
        if loop_exit:
            break
        
    
    
        
        
    
    

if __name__ == "__main__":
    main()
    




