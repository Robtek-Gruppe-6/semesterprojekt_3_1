from datalink import datareceiver, datalinker
from speaker import spk


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
        