


class Transport:
    def __init__(self, crc = True, segment = []):
        self.crc = crc
        self.segment = segment
        pass
    
    def reciver_flowcontrol(self, crc, segment):
        #Reciver side
        data = segment
        if(crc == True):
            return True, data
        
        elif(crc == False):
            return False, data
        
    def transmitter_flowcontrol(self,)
        