from speaker import spk
import time
class Datalink():
    
    def __init__(self):
        self.start_flag = '1010'  #Start flag binary sequence A 
        self.stop_flag = '1011'   #Stop flag binary sequence B
        self.collecting = False       #Tracks if we are currently collecting data
        self.data_buffer = []         #Buffer to store data between flags
        self.data_length = None
        
    def CRC8(self, data_bytes):
        polynomial = 0x07 #Translates to 0000 0111 or x^2 + x^1 + x^0
        crc = 0
        for byte in data_bytes:
            crc ^= byte #XOR gate
            for _ in range(8):  #Process each bit
                if crc & 0x80:  #If the leftmost bit is set
                    crc = (crc << 1) ^ polynomial 
                else:
                    crc <<= 1
                crc &= 0xFF  #Ensure CRC remains 8 bits
                
        print (hex(crc)[2:].zfill(2))
        return hex(crc)[2:].zfill(2)  #Convert to hex and zero-pad to 2 characters
    
    
datalinker = Datalink()
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
        
        #Start byte detection
        if (binary_val == 0xA or binary_val == 0xC) and not self.start_byte:
            print("Start-byte detected.")
            self.start_byte = True
            self.start_buff.append(hex(binary_val)[2:].upper())
            return None, [], [], []
        
        #Length byte detection
        if self.start_byte:
            if not self.len1_bool:  #First length byte
                self.len1 = binary_val
                if(self.len1 != None):
                    self.len1_bool = True
                    self.len_list.append(hex(self.len1)[2:].upper())
                    print(f"Length byte 1 received: {self.len1}")
            elif not self.len2_bool:  #Second length byte
                self.len2 = binary_val
                if(self.len2 != None):
                    self.length_val = (self.len1 << 4) | self.len2  #Combine length bytes
                    self.len2_bool = True
                    self.len_list.append(hex(self.len2)[2:].upper())
                    print(f"Length byte 2 received: {self.len2}, Total length: {self.length_val}")
            elif self.counter < self.length_val:  #Collect data based on length
                if(binary_val != None):
                    self.data += hex(binary_val)[2:].upper()  #Append as hex string
                    self.data_list.append(hex(binary_val)[2:].upper())  #Append as hex string
                    print(self.data_list)
                    self.counter += 1

            #Data collection complete
            if self.counter == self.length_val and not self.counting_done:  #Stop when all data is received
                self.counting_done = True
                return None, [], [], []

            #CRC byte collection
            if self.counting_done:
                if not self.crc1_bool and binary_val != None:  #First CRC byte
                    self.crc1 = hex(binary_val)[2:].upper() 
                    self.crc1_bool = True
                    print(f"CRC byte 1 received: {self.crc1}")
                elif not self.crc2_bool and binary_val != None:  #Second CRC byte
                    self.crc2 = hex(binary_val)[2:].upper() 
                    self.crc_val = f"{self.crc1}{self.crc2}".zfill(2)  #Combine CRC bytes
                    self.crc2_bool = True
                    print(f"CRC byte 2 received: {self.crc2}, CRC value: {self.crc_val}")
                    return None, [], [], []

            if self.crc2_bool and binary_val == 0xB:
                print("Stop byte detected: Data-frame complete.")
                print(bytearray.fromhex(self.data.zfill(8)))
                actual_crc = datalinker.CRC8(bytearray.fromhex(self.data.zfill(8))).upper()
                #Convert data_list to bytearray

                if(self.crc_val.zfill(2) == actual_crc):
                    print("CRC matches.")
                    self.crc_boolean = True
                    crccheck = self.crc_boolean

                #Store the result to return after resetting
                length = self.len_list 
                datasegment = self.data_list
                startflag = self.start_buff

                #Reset all variables for new data-frame
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
