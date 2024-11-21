
#NOT CURRENTLY IN USE
class ResponderCommands(): #Burde skifte navn på class
    def __init__(self, data = []):
        self.data = data

    def parse_data(self, data):
        n_mode = 1

        mode = data[:n_mode]  # First `n_mode` nibbles
        distance = int(data[n_mode:])  # Next `n_distance` nibbles
        
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