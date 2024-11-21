


class Transport:
    def __init__(self, crc = True, segment = []):
        self.crc = crc
        self.segment = segment
        pass
    
    def receiver_flowcontrol(self, crc, segment):
        #Reciver side
        data = segment
        if crc:
            mode, distance = self.parse_segment(segment)
            return True, mode, distance
        
        elif(crc == False):
            return False, None, None
        
    #def transmitter_flowcontrol(self,)
    
    def parse_segment(self, segment): #Skal nok være præsentatnions lag :D
        n_mode = 1  

        mode = segment[:n_mode]  # First `n_mode` nibbles
        distance = segment[n_mode:]  # Next `n_distance` nibbles

        return mode, distance
        
        

transport = Transport()


