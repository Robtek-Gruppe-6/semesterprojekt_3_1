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

    def length_byte(self, binary_len=0):
        hex_len = hex(binary_len)
        stripped_hex = hex_len[2:]
        hex_list = list(stripped_hex)
        if(len(stripped_hex) == 1):
            spk.play_dtmf_tone("0")
            print("0")
        for i in hex_list:
            print(i)
            spk.play_dtmf_tone(i)


    def send_binary_string(self, binary):
        binary_list = list(binary)
        binary_len = len(binary_list)
        self.start_sqn()             # Start byte
        self.length_byte(binary_len) # Length byte
        for i in binary_list:
            spk.play_dtmf_tone(i)    # Payload byte
        #CRC_stuff = datalinker.CRC8(binary_list) # CRC byte
        #print(CRC_stuff)
        self.stop_sqn()              # Stop byte

    def hello(self):
        self.send_binary_string()


    def input_binary(self):
        input_string = input("Input binary string: ")
        self.send_binary_string(input_string)

framer = Transport() # Laver instans til main