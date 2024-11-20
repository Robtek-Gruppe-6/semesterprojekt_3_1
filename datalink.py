class Datalink():
    
    def __init__(self):
        self.start_flagA = '1010'  # Start flag binary sequence A 
        self.start_flagC = '1100'  # Start flag binary sequence C
        self.stop_flag = '1011'   # Stop flag binary sequence B
        self.collecting = False       # Tracks if we are currently collecting data
        self.data_buffer = []         # Buffer to store data between flags
        self.data_length = None
        self.data_oddeven = None
        
    def CRC8(self, data_bytes):
        polynomial = 0x07 # Translates to 1000 0111 or x^8 + x^2 + x + 1
        crc = 0
        for byte in data_bytes:
            crc ^= byte # XOR gate
            for _ in range(8):  # Process each bit
                if crc & 0x80:  # If the leftmost bit is set
                    crc = (crc << 1) ^ polynomial 
                else:
                    crc <<= 1
                crc &= 0xFF  # Ensure CRC remains 8 bits

        return hex(crc)[2:].zfill(2)  # Convert to hex and zero-pad to 2 characters
       

    def receive_data(self, data):  # Binary data bliver nok en liste
        binary_data = format(data, '04b')

        
        if self.collecting == False:
            # Listen for start flag
            if binary_data == self.start_flagA:
                print("Start flag detected. Beginning data collection.") #Decoding
                self.collecting = "reading_length"
                self.data_buffer = []  # Clear buffer for new data
                self.data_oddeven = 'A'
                
            elif binary_data == self.start_flagC:
                print("Start flag detected. Beginning data collection.") #Decoding
                self.collecting = "reading_length"
                self.data_buffer = []  # Clear buffer for new data
                self.data_oddeven = 'B'
                
                
                
        elif self.collecting == "reading_length":
                if self.data_length is None:
                    self.data_length = int(binary_data, 2)
                else:
                    self.data_length = (self.data_length << 4) | int(binary_data, 2)
                    print(f"Data length: {self.data_length}")
                    self.collecting = True
                
        else:
            # Listen for stop flag to end data collection
            if binary_data == self.stop_flag:
                print("Stop flag detected. Ending data collection.")
                collected_data = self.data_buffer.copy()  # Copy buffer content for processing
                self.collecting = False  # Reset to listen for a new start flag
                self.data_buffer = []    # Clear buffer
                data_length = self.data_length
                self.data_length = None
                return collected_data, data_length, self.data_oddeven    # Return collected data for processing
            else:
                # Add incoming data to the buffer
                self.data_buffer.append(binary_data)
                print(f"Data added: {binary_data}")
        
        return None  # No data to return unless the stop flag is detected
    
    
    
datalinker = Datalink()
#hardware_data_stream = [10, 3, 2 , 2, 11]  # 3 and 2 represent length 0b0011 0010 -> 50

# Test the Datalink class with the hardware data stream
#for data in hardware_data_stream:
#    result = datalinker.receive_data(data)
#    if result:
#        collected_data, data_length = result
#        # Print collected data and data length for verification
#        print("Collected Data:", [bin(int(b, 2))[2:].zfill(4) for b in collected_data])
#        print("Data Length:", data_length)
