import time
from mqtt_pub import publish_command

class RobotControl():
    def __init__(self, mode = [], distance = []):
        self.mode = mode
        self.distance = distance
        self.commandBlockList = []
        self.speed = 0.10
        
    def controlRobot(self, mode, distance):
        if mode == 0b0001: #1 is drive
            publish_command(self.speed, 0.0)
            time.sleep(distance/self.speed)
            publish_command(0.0, 0.0)
            print(f"Published linear velocity: {distance}")
            
        elif mode == 0b0010: #2 is turn
            publish_command(0.0, self.speed)
            time.sleep(distance/self.speed)
            publish_command(0.0, 0.0)
            print(f"Published angular velocity: {distance}")


robot = RobotControl()