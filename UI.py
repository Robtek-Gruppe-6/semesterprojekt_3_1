class UI():
    def __init__(self):
        pass
    
    def ui(self):
        print("Welcome to the Robot Control System")

        #Ask for mode
        mode = input("Please select mode: \n1. Drive \n2. Turn \n3. Send commands\n")

        if mode == "1":
            print("Drive mode selected")
            #Ask for direction
            direction = input("Please select direction: \n1. Forward \n2. Backward \n")

            if direction == "1":
                print("Please enter distance in centimeters: ")
                distance = input()
                print ("Stacking command to drive forward " + distance + " centimeters")
                return "A" + distance #Returns the command in the format "A" + distance
            
            elif direction == "2":
                print( "Please enter distance in centimeters: ")
                distance = input()
                print("Stacking command to drive backward " + distance + " centimeters")
                return "B" + distance #Returns the command in the format "B" + distance
            
            else:
                print("Invalid input")

        if mode == "2":
            print("Turn mode selected")
            #Ask for direction
            direction = input("Please select direction: \n1. Right \n2. Left \n")

            if direction == "1":
                print("Please enter degrees to turn: ")
                degrees = input()
                print("Stacking command to turn right " + degrees + " degrees")
                return "C" + degrees #Returns the command in the format "C" + degrees
            
            elif direction == "2":
                print("Please enter degrees to turn: ")
                degrees = input()
                print("Stacking command to turn left " + degrees + " degrees")
                return "D" + degrees #Returns the command in the format "D" + degrees
            
            else:
                print("Invalid input")

        if mode == "3":
            print("Sending all commands")
            return "E"  #Returns the command "E" to send all commands
            
UI().ui()