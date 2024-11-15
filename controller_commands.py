#Controller side
class ControllerCommands():
    def __init__(self, data = []):
        self.data = data
        self.commandList = {
            (0b1110,0b1110): ("Error"), (0b1111,0b1111): ("Ack") 
        }

    def listOfCommands(self, data):

        if(self.data == [0b1110,0b1110]):
            return self.commandList.items(0)

        if(self.data == [0b1111,0b1111]):
            return self.commandList.items(1)