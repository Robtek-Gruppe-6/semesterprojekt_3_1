from datalink import datareceiver, datalinker
from speaker import spk
import time


class Transport:
    def __init__(self, crc_value = "00", crc = False, segment = []):
        self.crc = crc
        self.segment = segment
        self.crc_value = crc_value
        self.prev_parity = []
        self.prev_lebel = 0
        pass
    
    def reciver_flowcontrol(self, no_error_detected, parity = "A", length = ['0', '0'], datadata = ['0']):
        if((no_error_detected) and (parity != self.prev_parity[-1])):
            self.prev_parity.append(parity)
            return datadata
        elif(not no_error_detected and parity != self.prev_parity[-1]):
            self.prev_parity.append(parity)
            # Send no ACK
        elif(no_error_detected and parity == self.prev_parity[-1]):
            # Send ACK
            pass

    def transport_timer(self, capture_audio_func):
        start_time = time.time()
        while time.time() - start_time <= 5:  # 5 seconds timeout
            for audio_chunk in capture_audio_func():
                frequencies, magnitude = fil.analyze_frequency(audio_chunk)
                binary_value = decoder.process_chunk(frequencies, magnitude)
                if binary_value == "F":  # Assuming 'ACK' is the binary value for acknowledgment
                    return "Ack"
        return "Error"

    #def transport_timer(self, ack):
    #    start_time = time.time()
    #    while(time.time() - start_time <= 5):
    #        if(ack == True):
    #            return "Ack"
    #    return "Error"

    def transmitter_add_label(self, data):
        new_data = []
        if(self.prev_lebel == 0):
            new_data.append(1)
            new_data.append(data)
            self.prev_lebel = 1
        elif(self.prev_lebel == 1):
            new_data.append(0)
            new_data.append(data)
            self.prev_lebel = 0
        return new_data
            
        
flowcontrol = Transport()
    #def transmitter_flowcontrol(self,)
        