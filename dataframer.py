from speaker import spk
from decoding import decoder
from datalink import datalinker

class Transport():
    def __init__(self):
        self.start_flag = "10101010"  # Start flag binary sequence A A
        self.stop_flag = "10111011"   # Stop flag binary sequence B B

    def start_sqn(self):
        spk.play_dtmf_tone("A")
        return "A"
        
    def stop_sqn(self):
        spk.play_dtmf_tone("B")
        return "B"

    def play_all_tones(self, data_list):
        for i in data_list:
            spk.play_dtmf_tone(i.upper())
        

    def length_byte(self, binary_len=0):
        hex_len = hex(binary_len)
        stripped_hex = hex_len[2:]
        zfilled = stripped_hex.zfill(2)
        self.play_all_tones(zfilled)
        return zfilled

    def split_into_chunks(self, data, chunk_size=8):
        #print(f"data: {data}")
        # Pad the string with leading zeros to ensure its length is a multiple of chunk_size
        padded_data = data.zfill((len(data) + chunk_size - 1) // chunk_size * chunk_size)
        
        # Split the string into chunks of `chunk_size` characters
        chunks = [padded_data[i:i + chunk_size] for i in range(0, len(padded_data), chunk_size)]

        formatted_output = " ".join(chunks)
        
        return formatted_output

    def crc_byte(self, data):
            data_string = self.split_into_chunks(data)
            data_bytes = bytearray.fromhex(data_string)
            crc_output = datalinker.CRC8(data_bytes)
            #print(f"CRC output: {crc_output}")
            self.play_all_tones(crc_output)
            return crc_output.upper()


    def send_binary_string(self, binary_string):
        binary_list = list(binary_string)
        binary_len = len(binary_list)

        v1 = self.start_sqn()                 # Start byte
        v2 = self.length_byte(binary_len)     # Length byte
        v3 = self.play_all_tones(binary_list) # Payload byte(s)
        v4 = self.crc_byte(binary_string)     # CRC byte
        v5 = self.stop_sqn()                  # Stop byte
        print(f"Following dataframe was sent: {v1 + v2 + binary_string + v4 + v5}")

    def hello(self):
        self.send_binary_string("1")


    def input_binary(self):
        input_string = input("Input binary string: ")
        self.send_binary_string(input_string)

framer = Transport() # Laver instans til main