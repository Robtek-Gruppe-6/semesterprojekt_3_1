class PresentationLayer:
    def __init__(self):
        self.commands = ['F']  #List of commands

    def return_ack(self, ackchecked):
        if ackchecked:
            return self.commands[0]
        else:
            return None
    
    def parse_data(self, data):
        mode = data[0]  #First nibble is the mode
        if mode == 'E':
            return mode, 0
        distance_int = int(data[1:])

        return mode, distance_int

   
presentation_layer = PresentationLayer()
