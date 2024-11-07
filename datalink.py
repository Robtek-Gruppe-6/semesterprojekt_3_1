
class Datalink():
    
    def __init__(self):
        self.start_flag = "10101010"  # Start flag binary sequence A A
        self.stop_flag = "10111011"   # Stop flag binary sequence B B
        self.collecting = False       # Tracks if we are currently collecting data
        self.data_buffer = []         # Buffer to store data between flags

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
