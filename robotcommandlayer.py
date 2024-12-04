class PresentationLayer:
    def __init__(self):
        self.commands = ['F']  # List of commands

    def return_ack(self, ackchecked):
        if ackchecked:
            return self.commands[0]
        else:
            return None
        

   

# Example usage:
# Assuming transport_layer is an instance of a class that has a receive method
# transport_layer = TransportLayer()
presentation_layer = PresentationLayer()
# presentation_layer.receive_message()