
#NOT CURRENTLY IN USE
class ResponderCommands():
    def __init__(self, mode = [], distance = []):
        self.mode = mode
        self.distance = distance
        self.modeList = {
            (0b0001): ("Drive"), (0b0010): ("Turn") 
        }
        self.commandBlockList = []
    
    def makeCommand(self, mode, distance):
        command = self.modeList.get(mode)
        commandEntry = (command, distance)
        self.commandBlockList.append(commandEntry)
    
    def commandBlock(self):
        return self.commandBlockList