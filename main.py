#from control import *
from decoding import decoder
from filter import fil
from speaker import spk
from microphone import micro
from datalink import datareceiver
from transport import flowcontrol
#from plotting import plot
from UI import ui
#from datalink import datalinker
from dataframer import framer
#from mqtt_pub import publish_command, start_mqtt, stop_mqtt #Importing the neccecary functions from mqtt_pub.py

def main():
    
    #Transmitter side
    while True:
        loop_exit = ui.interface()
        data = ui.datalist
        segment = flowcontrol.transmitter_add_label(data)
        frame = framer.build_frame(segment)
        print(f"Frame: {frame}")
        spk.play_list_of_tones(frame)
        ui.datalist = []
        if loop_exit:
            break
    

if __name__ == "__main__":
    main()
    




