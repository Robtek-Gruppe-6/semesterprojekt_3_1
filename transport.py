from datalink import datareceiver, datalinker
from speaker import spk
import time
import threading


class Transport:
    def __init__(self, crc_value="00", crc=False, segment=[]):
            self.crc = crc
            self.segment = segment
            self.crc_value = crc_value
            self.prev_parity = 0
            self.prev_lebel = 0 #Fix bug with parity
    
    #ROBOT
    def receiver_flowcontrol(self, crc, datasegment = ['0']):
            
        parity = datasegment[0]
        if((crc) and (parity != self.prev_parity)):
            self.prev_parity = parity
            print("ACK, saved") #debug
            return True, datasegment[1:]
        elif(not crc):
            #self.prev_parity = parity
            # Send no ACK
            print("NO ACK") #debug
            return False, None
        elif(crc and parity == self.prev_parity):
            self.prev_parity ^= 1
            self.prev_lebel = parity
            # Send ACK
            print("ACK, disc") #debug
            return True, None
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
        