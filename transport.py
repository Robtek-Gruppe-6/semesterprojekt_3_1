from speaker import spk

class Transport():
    def __init__(self):
        self.start_flag = "10101010"  # Start flag binary sequence A A
        self.stop_flag = "10111011"   # Stop flag binary sequence B B

    def start_sqn(self):
        spk.play_dtmf_tone("A")
        
    def stop_sqn(self):
        spk.play_dtmf_tone("B")


    def send_binary_string(self, binary):
        binary_list = list(binary)
        binary_len = len(binary_list)
        self.start_sqn()   
        for i in binary_list:
            spk.play_dtmf_tone(i)
        self.CSC(binary_len)
        self.stop_sqn()

    def hello(self):
        self.send_binary_string()


    def input_binary(self):
        input_string = input("Input binary string: ")
        self.send_binary_string(input_string)

trans = Transport() # Laver instans til main