from speaker import spk

class Control:
    def __init__(self):
        pass

    def drive_mode(self, distance):
        print("Drive mode activated")
        spk.play_dtmf_tone('1')  # Bind DTMF tone '1' to drive mode
        self.distance_mode(distance)

    def rotate_mode(self):
        print("Rotate mode activated")
        spk.play_dtmf_tone('2')  # Bind DTMF tone '2' to rotate mode
        
    def distance_mode(self, distance):
        print(f"Distance mode activated with distance: {distance}")
        spk.play_dtmf_tone('A')
        spk.play_dtmf_tone(str(distance))

if __name__ == "__main__":
    control = Control()
    #control.drive_mode()
    #control.rotate_mode()
    #control.distance_mode()
    