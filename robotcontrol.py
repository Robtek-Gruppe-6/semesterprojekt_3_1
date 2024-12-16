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
                #reverse = self.reverseMapping(self.commandBlockList) #Virker ikke helt endnu men burde være simpelt nok at fikse lige nu laver den fejl i parity
                #self.commandBlockList.extend(reverse)
                print(self.commandBlockList)
                for command in self.commandBlockList:
                    cmd_mode, cmd_distance = command
                    if cmd_mode == 'A': #A is drive
                        publish_command(self.speed, 0.0)
                        time.sleep((cmd_distance/100)/self.speed)
                        publish_command(0.0, 0.0)
                        #print(f"Published linear velocity: {cmd_distance}")
                        
                    elif cmd_mode == 'B': #B is drive backwards
                        publish_command(-self.speed, 0.0)
                        time.sleep((cmd_distance/100)/self.speed)
                        publish_command(0.0, 0.0)    

                    elif cmd_mode == 'C': #C is turn right
                        publish_command(0.0, -self.speed)
                        time.sleep((cmd_distance*(math.pi/180))/self.speed)
                        publish_command(0.0, 0.0)
                        #print(f"Published angular velocity: {cmd_distance}")
                    
                    elif cmd_mode == 'D': #D is turn left
                        publish_command(0.0, self.speed)
                        time.sleep((cmd_distance*(math.pi/180))/self.speed)
                        publish_command(0.0, 0.0)
                        #print(f"Published angular velocity: {cmd_distance}")
                        
                    elif cmd_mode == 'F': #F is wait
                        publish_command(0.0, 0.0)
                        time.sleep(cmd_distance)

                self.commandBlockList.clear() # Outcomment this line to keep the commands in the list

            elif mode != 'E':
                self.commandBlockList.append((mode, distance))
                print(f"Command added: mode={mode}, distance={distance}")
                
    def reverseMapping(self, commandList):
        retlist = [("C", "1", "8", "0")]
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
        retlist.extend(self.commandReverseBlockList) 
        return retlist


robot = RobotControl()