#Controller side
class ControllerCommands():
    def __init__(self, transport_layer):
        self.transport_layer = transport_layer
        self.commands = ['F']  # List of commands

    def process_ack(self, ack):
            if ack == self.commands[0]:
                print("ACK received for command 'F'")
                retur