#import crc
from speaker import spk
import time
class Datalink():
    
    def __init__(self):
        self.start_flag = '1010'  # Start flag binary sequence A 
        self.stop_flag = '1011'   # Stop flag binary sequence B
        self.collecting = False       # Tracks if we are currently collecting data
        self.data_buffer = []         # Buffer to store data between flags
        self.data_length = None
        
    def CRC8(self, data_bytes):
        polynomial = 0x07 # Translates to 0000 0111 or x^2 + x^1 + x^0
        crc = 0
        for byte in data_bytes:
            crc ^= byte # XOR gate
            for _ in range(8):  # Process each bit
                if crc & 0x80:  # If the leftmost bit is set
                    crc = (crc << 1) ^ polynomial 
                else:
                    crc <<= 1
                crc &= 0xFF  # Ensure CRC remains 8 bits
                
        print (hex(crc)[2:].zfill(2))
        return hex(crc)[2:].zfill(2)  # Convert to hex and zero-pad to 2 characters
    
    

    def receive_data(self, data):  # Binary data bliver nok en liste
        binary_data = (data) #format(data, '04b')

        
        if self.collecting == False:
            # Listen for start flag
            if binary_data == self.start_flag:
                print("Start flag detected. Beginning data collection.") #Decoding
                self.collecting = "reading_length"
                self.data_buffer = []  # Clear buffer for new data
                
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
                return collected_data, data_length    # Return collected data for processing
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

class Receiver():
    def __init__(self):

        self.start_byte = False
        self.start_buff = []
        self.counter = 0
        self.len1_bool = False
        self.len2_bool = False
        self.crc1_bool = False
        self.crc2_bool = False
        self.crc_boolean = False
        self.len_list = []
        self.data_list = []
        self.data = ""
        self.counting_done = False
        self.length_val = 255
        self.start_time = 0



    def frame_receiver(self, binary_val):
        crccheck = False
        
        if(binary_val != None):
            self.start_time = time.time()
            
        if(self.start_byte and self.start_time != 0 and time.time() > self.start_time + 2):
            self.start_byte = False
            self.counter = 0
            self.len1_bool = False
            self.len2_bool = False
            self.crc1_bool = False
            self.crc2_bool = False
            self.crc_boolean = False
            self.counting_done = False
            self.length_val = 255
            self.len_list = []
            self.data_list = []
            self.start_buff = []
            self.start_time = 0
            self.data = ""
            print("Error detected: Timer expired.")
            
            return None, [], [], []
        
        # Start byte detection
        if (binary_val == 0xA or binary_val == 0xC) and not self.start_byte:
            print("Start-byte detected.")
            self.start_byte = True
            self.start_buff.append(hex(binary_val)[2:].upper())
            return None, [], [], []
        
        # Length byte detection
        if self.start_byte:
            if not self.len1_bool:  # First length byte
                self.len1 = binary_val
                if(self.len1 != None):
                    self.len1_bool = True
                    self.len_list.append(hex(self.len1)[2:].upper())
                    print(f"Length byte 1 received: {self.len1}")
            elif not self.len2_bool:  # Second length byte
                self.len2 = binary_val
                if(self.len2 != None):
                    self.length_val = (self.len1 << 4) | self.len2  # Combine length bytes
                    self.len2_bool = True
                    self.len_list.append(hex(self.len2)[2:].upper())
                    print(f"Length byte 2 received: {self.len2}, Total length: {self.length_val}")
            elif self.counter < self.length_val:  # Collect data based on length
                if(binary_val != None):
                    self.data += hex(binary_val)[2:].upper()  # Append as hex string
                    self.data_list.append(hex(binary_val)[2:].upper())  # Append as hex string
                    print(self.data_list)
                    self.counter += 1

            # Data collection complete
            if self.counter == self.length_val and not self.counting_done:  # Stop when all data is received
                self.counting_done = True
                return None, [], [], []

            # CRC byte collection
            if self.counting_done:
                if not self.crc1_bool and binary_val != None:  # First CRC byte
                    self.crc1 = hex(binary_val)[2:].upper() #hex(int(binary_val))[2:].upper()
                    self.crc1_bool = True
                    print(f"CRC byte 1 received: {self.crc1}")
                elif not self.crc2_bool and binary_val != None:  # Second CRC byte
                    self.crc2 = hex(binary_val)[2:].upper() #hex(int(binary_val))[2:].upper()
                    self.crc_val = f"{self.crc1}{self.crc2}".zfill(2)  # Combine CRC bytes
                    self.crc2_bool = True
                    print(f"CRC byte 2 received: {self.crc2}, CRC value: {self.crc_val}")
                    return None, [], [], []

            if self.crc2_bool and binary_val == 0xB:
                print("Stop byte detected: Data-frame complete.")
                print(bytearray.fromhex(self.data.zfill(8)))
                actual_crc = datalinker.CRC8(bytearray.fromhex(self.data.zfill(8))).upper()
                # Convert data_list to bytearray
                
                
                #print(f"CRC value: {self.crc_val.zfill(2)}" + f" Actual CRC: {actual_crc}")

                if(self.crc_val.zfill(2) == actual_crc):
                    print("CRC matches.")
                    self.crc_boolean = True
                    crccheck = self.crc_boolean
                    
                
                #entire_frame = f"A{str(self.length_val).zfill(2)}" + f"{self.data}" + f"{self.crc_val}B"
                #print(list(entire_frame))
                #actual_crc = datalinker.CRC8(bytearray.fromhex(self.data.zfill(8))).upper()
                #print(f"CRC value: {self.crc_val.zfill(2)}" + f" Actual CRC: {actual_crc}")

                #if(self.crc_val.zfill(2) == actual_crc):
                #    print("CRC matches.")

                # Store the result to return after resetting
                length = self.len_list 
                datasegment = self.data_list
                startflag = self.start_buff

                # Reset all variables for new data-frame
                self.start_byte = False
                self.counter = 0
                self.len1_bool = False
                self.len2_bool = False
                self.crc1_bool = False
                self.crc2_bool = False
                self.crc_boolean = False
                self.counting_done = False
                self.length_val = 255
                self.len_list = []
                self.data_list = []
                self.start_buff = []
                self.data = ""
                
                
                return crccheck, startflag, length, datasegment
    
        return None, [], [], []
            
datareceiver = Receiver()
