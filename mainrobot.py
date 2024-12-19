from microphone import micro
from speaker import spk
from datalink import datareceiver
from decoding import decoder
from filter import fil
from transport import flowcontrol
from dataframer import framer
from robotcommandlayer import presentation_layer
from robotcontrol import robot
import time


from mqtt_pub import publish_command, start_mqtt, stop_mqtt #Importing the neccecary functions from mqtt_pub.py

def sending_stack(data):
      segment = flowcontrol.transmitter_add_label(data)
      frame = framer.build_frame(segment)
      print(f"Frame: {frame}")
      spk.play_list_of_tones(frame)


def main():
   start_mqtt() #Start the MQTT client
    
   try:
      for audio_chunk in micro.capture_audio():
         
         filtered_chunk = fil.butter_bandpass(audio_chunk)
         frequencies, magnitude = fil.analyze_frequency(filtered_chunk)
         binary_val = decoder.process_chunk(frequencies, magnitude)
         
         crc, _, _, datasegment  = datareceiver.frame_receiver(binary_val)
         if not datasegment and (crc == None):
            continue
         #print(crc)
         #print(datasegment)
         
         ackchecked, data_rob = flowcontrol.receiver_flowcontrol(crc, datasegment)
         #print (ackchecked)
         #print (data_rob)
         if not ackchecked:
            continue

         command = presentation_layer.return_ack(ackchecked)
         time.sleep(0.8)
         sending_stack(command)

         if not data_rob:
            continue

         mode, distance = presentation_layer.parse_data(data_rob)

         robot.controlRobot(mode, distance)
           
           
           
   finally:
      micro.close()
      #stop_mqtt() #Stop the MQTT client
        
        


if __name__ == "__main__":
    main()