class PresentationLayer:
    def __init__(self):
        self.commands = ['F']  # List of commands

    def return_ack(self, ackchecked):
        if ackchecked:
            return self.commands[0]
        else:
            return None
    
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
                 distance_mapped += str(extended_mapping[char])  # Replace with mapped value
            else:
                distance_mapped += char  # Keep numeric values as is

        # Convert the mapped distance string to an integer
        distance_int = int(distance_mapped)

        return mode, distance_int

   

# Example usage:
# Assuming transport_layer is an instance of a class that has a receive method
# transport_layer = TransportLayer()
presentation_layer = PresentationLayer()
# presentation_layer.receive_message()