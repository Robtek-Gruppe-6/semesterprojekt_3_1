from datalink import datareceiver, datalinker
from speaker import spk


class Transport:
    def __init__(self, crc_value = "00", crc = False, segment = []):
        self.crc = crc
        self.segment = segment
        self.crc_value = crc_value
        self.prev_parity = []
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
            
            
        
flowcontrol = Transport()
    #def transmitter_flowcontrol(self,)
        