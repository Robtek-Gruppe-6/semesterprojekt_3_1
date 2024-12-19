from speaker import spk
from datalink import datalinker

class Dataframing():
    def __init__(self):
        self.tones = []

    def start_sqn(self):
            self.tones.append("A")
        
    def stop_sqn(self):
        self.tones.append("B")

    def length_byte(self, binary_data):
        binary_len = len(binary_data)
        hex_len = hex(binary_len)[2:]
        hex_len = hex_len.zfill(2)
        self.tones.extend(list(hex_len))
        
        return hex_len

    def split_into_chunks(self, binary_data, chunk_size=8):
        #Pad the string with leading zeros to ensure its length is a multiple of chunk_size
        
        binary_str = ''.join(binary_data)
        
        padded_data = binary_str.zfill((len(binary_str) + chunk_size - 1) // chunk_size * chunk_size)
        
        #Split the string into chunks of `chunk_size` characters
        chunks = [padded_data[i:i + chunk_size] for i in range(0, len(padded_data), chunk_size)]

        formatted_output = " ".join(chunks)
        
        return formatted_output

    def crc_byte(self, data):
            data_string = self.split_into_chunks(data)
            data_bytes = bytearray.fromhex(data_string)
            crc_output = datalinker.CRC8(data_bytes)
            crc_output_upper = crc_output.upper()
            
            self.tones.extend(list(crc_output_upper))
            return crc_output.upper()

    def input_binary(self):
        input_string = input("Input binary string: ")
        self.send_binary_string(input_string)
        
    
    def build_frame(self, binary_data):
        #Clear
        self.tones = []
        
        #Start flag
        self.start_sqn() 
        
        #Length
        self.length_byte(binary_data)
        
        #Actual data
        self.tones.extend(binary_data)
        
        #CRC
        self.crc_byte(binary_data) 
        
        #stop flag
        self.stop_sqn() 

        return self.tones
    
    

framer = Dataframing()
