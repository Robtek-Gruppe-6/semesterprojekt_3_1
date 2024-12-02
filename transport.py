from datalink import datareceiver, datalinker
from speaker import spk
import time
import threading


class Transport:
    def __init__(self, crc_value="00", crc=False, segment=[]):
            self.crc = crc
            self.segment = segment
            self.crc_value = crc_value
            self.prev_parity = []
            self.prev_lebel = 0
    
    #ROBOT
    def receiver_flowcontrol(self, no_error_detected, datasegment = ['0']):
        parity = datasegment[0]
        if((no_error_detected) and (parity != self.prev_parity)):
            self.prev_parity = parity
            print("ACK") #debug
            return True, datasegment[1:]
        elif(not no_error_detected and parity != self.prev_parity):
            self.prev_parity = parity
            # Send no ACK
            print("NO ACK") #debug
            return False
        elif(no_error_detected and parity == self.prev_parity):
            # Send ACK
            print("ACK") #debug
            return True
#        
#    def transport_timer(self, capture_audio_func):
#        start_time = time.time()
#        while time.time() - start_time <= 5:  # 5 seconds timeout
#            for audio_chunk in capture_audio_func():
#                frequencies, magnitude = fil.analyze_frequency(audio_chunk)
#                binary_value = decoder.process_chunk(frequencies, magnitude)
#                if binary_value == "F":  # Assuming 'ACK' is the binary value for acknowledgment
#                    return "Ack"
#                return "Error"


        
    def transport_ack_check(self, binary_value):
        start_time = time.time()
        print("Timer started")
        while time.time() - start_time <= 5:  # Timeout after 5 seconds
            pass
        print("Timer expired")
        return False
            

    #Computer
    def computer_receiver_flowcontrol(self, crc, datasegment):
        if crc:
            return datasegment[1:]
        elif crc == False:
            # If there is an error, set prev_lebel to the same value to resend the same label
            self.prev_lebel = 1 - self.prev_lebel


    def transmitter_add_label(self, data):
        new_data = []
        if(self.prev_lebel == 0):
            new_data.append("1")
            new_data.extend(data)
            self.prev_lebel = 1
        elif(self.prev_lebel == 1):
            new_data.append("0")
            new_data.extend(data)
            self.prev_lebel = 0
        return new_data
            
        
flowcontrol = Transport()
    #def transmitter_flowcontrol(self,)
        