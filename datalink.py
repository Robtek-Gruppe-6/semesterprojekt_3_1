import crc
class Datalink():
    
    def __init__(self):
        self.start_flag = 1010  # Start flag binary sequence A
        self.stop_flag = 1011   # Stop flag binary sequence B
        self.collecting = False       # Tracks if we are currently collecting data
        self.data_buffer = []         # Buffer to store data between flags

    #def CRC8(self, data_list):
        # Convert the list of hex values into a byte array
        #data_bytes = bytearray()

        #for hex_value in data_list:
            # Convert each hex value (string) into an integer and append to the bytearray
        #    data_bytes.append(int(hex_value, 16))
        #print(data_bytes)

        # Calculate CRC-8 using the crc8 function from the library
        #crc_value = crc.Crc8(data_bytes)
        
        #return crc_value
            
    def receive_data(self, binary_data):  # Binary data bliver nok en liste
        
        if self.collecting == False:
            # Listen for start flag
            if binary_data == self.start_flag:
                print("Start flag detected. Beginning data collection.") #Decoding
                self.collecting = True
                self.data_buffer = []  # Clear buffer for new data
        else:
            # Listen for stop flag to end data collection
            if binary_data == self.stop_flag:
                print("Stop flag detected. Ending data collection.")
                collected_data = self.data_buffer.copy()  # Copy buffer content for processing
                self.collecting = False  # Reset to listen for a new start flag
                self.data_buffer = []    # Clear buffer
                return collected_data    # Return collected data for processing
            else:
                # Add incoming data to the buffer
                self.data_buffer.append(binary_data)
                print(f"Data added: {binary_data}")
        
        return None  # No data to return unless the stop flag is detected
    

datalinker = Datalink()
