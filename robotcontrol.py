import time
import math
from mqtt_pub import publish_command

class RobotControl():
    def __init__(self, mode = [], distance = []):
        self.mode = mode
        self.distance = distance
        self.commandBlockList = []
        self.commandReverseBlockList = []
        self.speed = 0.10

    def controlRobot(self, mode, distance):
            if mode == 'E':
                reverse = self.reverseMapping(self.commandBlockList) # Reverse the command list
                self.commandBlockList.extend(reverse) # Add the reversed list to the original list
                print(self.commandBlockList)
                for command in self.commandBlockList:
                    cmd_mode, cmd_distance = command
                    if cmd_mode == 'A': #A is drive
                        publish_command(self.speed, 0.0)
                        time.sleep((cmd_distance/100)/self.speed)
                        publish_command(0.0, 0.0)
                        
                    elif cmd_mode == 'B': #B is drive backwards
                        publish_command(-self.speed, 0.0)
                        time.sleep((cmd_distance/100)/self.speed)
                        publish_command(0.0, 0.0)    

                    elif cmd_mode == 'C': #C is turn right
                        publish_command(0.0, -self.speed)
                        time.sleep((cmd_distance*(math.pi/180))/self.speed)
                        publish_command(0.0, 0.0)
                    
                    elif cmd_mode == 'D': #D is turn left
                        publish_command(0.0, self.speed)
                        time.sleep((cmd_distance*(math.pi/180))/self.speed)
                        publish_command(0.0, 0.0)
                        
                    elif cmd_mode == 'F': #F is wait
                        publish_command(0.0, 0.0)
                        time.sleep(cmd_distance)

                #self.commandBlockList.clear() # Outcomment this line to keep the commands in the list

            elif mode != 'E': # adds a commands to the block list
                self.commandBlockList.append((mode, distance))
                print(f"Command added: mode={mode}, distance={distance}")
                
    def reverseMapping(self, commandList):
        retlist = [('C', 180)]
        print("Initial Reverse List: ", retlist)
        for command in commandList:
            mode, distance = command
            print (mode, distance)
            if mode == 'A':
                self.commandReverseBlockList.insert(0, ('A', distance))
            elif mode == 'B':
                self.commandReverseBlockList.insert(0, ('B', distance))
            elif mode == 'C':
                self.commandReverseBlockList.insert(0, ('D', distance))
            elif mode == 'D':
                self.commandReverseBlockList.insert(0, ('C', distance))
            else:
                self.commandReverseBlockList.insert(0, (mode, distance))
            print("Current Reverse List: ", self.commandReverseBlockList)
        retlist.extend(self.commandReverseBlockList) 
        print("Final Reverse List: ", retlist)
        return retlist


robot = RobotControl()