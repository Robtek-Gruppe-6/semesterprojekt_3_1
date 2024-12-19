
#NOT CURRENTLY IN USE
class ResponderCommands(): #Burde skifte navn på class
    def __init__(self, data = []):
        self.data = data

    def parse_data(self, data):
        n_mode = 1

        mode = data[:n_mode]  # First `n_mode` nibbles
        extended_mapping = {
            "A": 10,
            "B": 11,
            "C": 12,
            "D": 13,
            "*": 14,
            "#": 15
        }

        distance_hex = data[n_mode:]  # Remaining characters as distance

        # Convert distance_hex character by character using the extended_mapping
        distance_mapped = ""
        for char in distance_hex:
            if char in extended_mapping:
                distance_mapped += extended_mapping[char]  # Replace with mapped value
            else:
                distance_mapped += char  # Keep numeric values as is

        # Convert the mapped distance string to an integer
        distance_int = int(distance_mapped)

        return mode, distance_int
    
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