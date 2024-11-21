from datalink import datareceiver, datalinker
from speaker import spk


class Transport:
    def __init__(self, crc_value = "00", crc = False, segment = []):
        self.crc = crc
        self.segment = segment
        self.crc_value = crc_value
        self.count = 0
        pass
    
    def reciver_flowcontrol(self, segment):
        [result] = datareceiver.robot_receiver(segment)
        crc_value = result(1)
        data = result(2)
        calc_crc = datalinker.CRC8(data)

        # Receiver side
        if(crc_value == calc_crc):
            print("CRC check passed")
            # Send ACK
            #spk.play_dtmf_tone("A")
            #spk.play_dtmf_tone("0")
            #spk.play_dtmf_tone("1")
            #spk.play_dtmf_tone("F")
            #spk.play_dtmf_tone("A")
            # We need to tell session layer that we have a correct CRC value

            crc_value = ""
            data = ""
            return True
        
    def transmitter_oddeven(self):
        if self.count == 0:
            self.count = 1
            return 0
        elif self.count == 1:
            self.count = 0
            return 1
        
flowcontrol = Transport()
    #def transmitter_flowcontrol(self,)
        