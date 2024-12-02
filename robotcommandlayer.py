class PresentationLayer:
    def __init__(self, transport_layer):
        self.transport_layer = transport_layer
        self.commands = ['F']  # List of commands

    def receive_message(self, ack, data = []):
        message = self.transport_layer.receive()
        if ack:
            self.process_ack()
            #pass data to higher layer
        elif not ack:
            self.process_err()
        

    def process_ack(self):
        for command in self.commands:
            if command == 'F':
                print("ACK received for command 'F'")
                # Add further processing for 'F' command here

    def process_err(self):
        print("Error received, message discarded") 

# Example usage:
# Assuming transport_layer is an instance of a class that has a receive method
# transport_layer = TransportLayer()
presentation_layer = PresentationLayer()
# presentation_layer.receive_message()