from datalink import datareceiver


class Transport:
    def __init__(self, crc_value = "00", crc = False, segment = []):
        self.crc = crc
        self.segment = segment
        self.crc_value = crc_value
        pass
    
    def reciver_flowcontrol(self, segment):
        [data, crc] = datareceiver.robot_receiver(self, segment)
        # Receiver side
        if(crc == True):
            return True, data
        
        elif(crc == False):
            return False, data
        
    #def transmitter_flowcontrol(self,)
        