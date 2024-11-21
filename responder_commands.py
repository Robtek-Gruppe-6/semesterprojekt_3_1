
#NOT CURRENTLY IN USE
class ResponderCommands(): #Burde skifte navn på class
    def __init__(self, segment = []):
        self.segment = segment

    def parse_segment(self, segment):
        n_mode = 1  

        mode = segment[:n_mode]  # First `n_mode` nibbles
        distance = segment[n_mode:]  # Next `n_distance` nibbles

        distance = int(distance, 16) # Convert directly if the distance is numeric (0-9) or hex character (A-F)
        return mode, distance
    
    #def __init__(self, mode = [], distance = []):
    #    self.mode = mode
    #    self.distance = distance
    #    self.modeList = {
    #        (0b0001): ("Drive"), (0b0010): ("Turn") 
    #    }
    #    self.commandBlockList = []
    
    #def makeCommand(self, mode, distance):
    #    command = self.modeList.get(mode)
    #    commandEntry = (command, distance)
    #    self.commandBlockList.append(commandEntry)
    
    #def commandBlock(self):
    #    return self.commandBlockList