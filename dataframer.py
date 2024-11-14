from speaker import spk
from decoding import decoder
from datalink import datalinker

class Transport():
    def __init__(self):
        self.start_flag = "10101010"  # Start flag binary sequence A A
        self.stop_flag = "10111011"   # Stop flag binary sequence B B

    def start_sqn(self):
        spk.play_dtmf_tone("A")
        
    def stop_sqn(self):
        spk.play_dtmf_tone("B")

    def play_all_tones(self, data_list):
        for i in data_list:
            spk.play_dtmf_tone(i)
        

    def length_byte(self, binary_len=0):
        hex_len = hex(binary_len)
        stripped_hex = hex_len[2:]
        hex_list = list(stripped_hex)
        if(len(stripped_hex) == 1):
            spk.play_dtmf_tone("0")
            print("0")
        self.play_all_tones(hex_list)

    def crc_byte(self, data):
        # Step 1: Join the list of data items into a single string of hex values
        data_str = ''.join(data)

        # Step 2: Split the data into chunks of 8 characters (8 hex digits = 4 bytes)
        chunks = [data_str[i:i+8] for i in range(0, len(data_str), 8)]
        

        # Step 3: For each chunk, calculate the CRC8 and play the tones
        for chunk in chunks:
            # If the chunk is less than 8 characters, pad with leading zeros
            chunk = chunk.zfill(8)
            print(chunk)
            
            # Step 5: Calculate CRC for the current frame and play tones
            data_bytes = bytearray.fromhex(chunk)
            crc_output = datalinker.CRC8(data_bytes)
            self.play_all_tones(crc_output)


    def send_binary_string(self, binary):
        binary_list = list(binary)
        binary_len = len(binary_list)

        self.start_sqn()                 # Start byte
        self.length_byte(binary_len)     # Length byte
        self.play_all_tones(binary_list) # Payload byte(s)
        self.crc_byte(binary_list)       # CRC byte
        self.stop_sqn()                  # Stop byte

    def hello(self):
        self.send_binary_string()


    def input_binary(self):
        input_string = input("Input binary string: ")
        self.send_binary_string(input_string)

framer = Transport() # Laver instans til main