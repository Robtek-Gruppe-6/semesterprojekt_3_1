from microphone import micro
from speaker import spk
from datalink import datareceiver
from decoding import decoder
from filter import fil
from transport import flowcontrol
from dataframer import framer
from robotcommandlayer import presentation_layer



#from mqtt_pub import publish_command, start_mqtt, stop_mqtt #Importing the neccecary functions from mqtt_pub.py

def sending_stack(data):
      segment = flowcontrol.transmitter_add_label(data)
      frame = framer.build_frame(segment)
      print(f"Frame: {frame}")
      spk.play_list_of_tones(frame)


def main():
    #start_mqtt() #Start the MQTT client
    
   try:
      for audio_chunk in micro.capture_audio():
         filtered_chunk = fil.butter_bandpass(audio_chunk)
         frequencies, magnitude = fil.analyze_frequency(filtered_chunk)
         binary_val = decoder.process_chunk(frequencies, magnitude)
         
         
         

         crc, _, _, datasegment  = datareceiver.frame_receiver(binary_val)
         if not datasegment and (crc == None):
            continue
         print(crc)
         
         ackchecked, data_rob = flowcontrol.receiver_flowcontrol(crc, datasegment)
         if not ackchecked:
            continue
      
         command = presentation_layer.return_ack(ackchecked)
         sending_stack(command)
            
            #if binary_val is not None:
            #    result = datalinker.receive_data(binary_val)
            #    if result:
            #         
            #         collected_data, data_length = result
            #         print("Collected Data:", [bin(int(b, 2))[2:].zfill(4) for b in collected_data])
            #         print("Data Length:", data_length)
            
            #Check if the binary value corresponds to a DTMF tone '1' or '#'
            #if binary_val == 1: # Assuming '0001' is the binary value for '1'
            #    angular_velocity = 0.05 # Set the angular velocity to 0.05 rad/s
            #    publish_command(0.0, angular_velocity) # Publish the command to the MQTT topic
            #    print(f"Published angular velocity: {angular_velocity}")
            #elif binary_val == 2: #Assuming '0010' is the binary value for '2'
            #    linear_velocity = 0.05
            #    publish_command(linear_velocity, 0.0) # Publish the command to the MQTT topic
            #    print(f"Published linear velocity: {linear_velocity}")
            #elif binary_val == 15: #Assuming '1111' is the binary value for '#'
            #    publish_command(0.0, 0.0)
            #    print("Published stop command")
           
           #Check if the binary value corresponds to a DTMF tone '1' or '#'
      #      if binary_val == 1: # Assuming '0001' is the binary value for '1'
      #         angular_velocity = 0.05 # Set the angular velocity to 0.05 rad/s
      #         publish_command(0.0, angular_velocity) # Publish the command to the MQTT topic
      #         print(f"Published angular velocity: {angular_velocity}")
      #      elif binary_val == 2: #Assuming '0010' is the binary value for '2'
      #         linear_velocity = 0.15
      #         publish_command(linear_velocity, 0.0) # Publish the command to the MQTT topic
      #         print(f"Published linear velocity: {linear_velocity}")
      #      elif binary_val == 15: #Assuming '1111' is the binary value for '#'
      #         publish_command(0.0, 0.0)
      #         print("Published stop command")
           
           
           
   finally:
      micro.close()
      #stop_mqtt() #Stop the MQTT client
        
        


if __name__ == "__main__":
    main()