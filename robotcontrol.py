import time
from mqtt_pub import publish_command

class RobotControl():
    def __init__(self, mode = [], distance = []):
        self.mode = mode
        self.distance = distance
        self.commandBlockList = []
        self.speed = 0.10
        
#    def controlRobot(self, mode, distance):
#        if mode == 'E' and distance == 0:
#            gg
#
#        if mode == 'A': #A is drive
#            publish_command(self.speed, 0.0)
#            time.sleep(distance/self.speed)
#            publish_command(0.0, 0.0)
#            print(f"Published linear velocity: {distance}")
#
#        elif mode == 'C': #2 is turn
#            publish_command(0.0, self.speed)
#            time.sleep(distance/self.speed)
#            publish_command(0.0, 0.0)
#            print(f"Published angular velocity: {distance}")

    def controlRobot(self, mode, distance):
            if mode == 'E':
                for command in self.commandBlockList:
                    cmd_mode, cmd_distance = command
                    if cmd_mode == 'A': #A is drive
                        publish_command(self.speed, 0.0)
                        time.sleep(cmd_distance/self.speed)
                        publish_command(0.0, 0.0)
                        #print(f"Published linear velocity: {cmd_distance}")

                    elif cmd_mode == 'C': #C is turn right
                        publish_command(0.0, -self.speed)
                        time.sleep(cmd_distance/self.speed)
                        publish_command(0.0, 0.0)
                        #print(f"Published angular velocity: {cmd_distance}")
                    
                    elif cmd_mode == 'D': #D is turn left
                        publish_command(0.0, self.speed)
                        time.sleep(cmd_distance/self.speed)
                        publish_command(0.0, 0.0)
                        #print(f"Published angular velocity: {cmd_distance}")

                        

                self.comzmandBlockList.clear() # Outcomment this line to keep the commands in the list

            elif mode != 'E':
                self.commandBlockList.append((mode, distance/100))
                print(f"Command added: mode={mode}, distance={distance}")


robot = RobotControl()