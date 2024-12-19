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
            self.prev_lebel = 0
    
    #ROBOT
    def receiver_flowcontrol(self, crc, datasegment = ['0']):
            
        parity = int(datasegment[0])
        if((crc) and (parity != self.prev_parity)):
            self.prev_parity = parity
            print("ACK, saved")
            return True, datasegment[1:]
        elif(not crc):
            #Send no ACK
            print("NO ACK") 
            return False, None
        elif((crc) and (parity == self.prev_parity)):
            self.prev_lebel = 1 - self.prev_lebel
            #Send ACK
            print("ACK, disc") 
            return True, None
          

    #Computer
    def computer_receiver_flowcontrol(self, crc, datasegment):
        if crc:
            return datasegment[1:]
        elif crc == False:
            return None


    def transmitter_add_label(self, data): #Parity flipping
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
        