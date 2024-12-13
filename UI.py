class UI():
    def __init__(self):
        self.datalist = []
        
    
    def interface(self):
        print("Welcome to the Robot Control System") 
   
            
        mode = input("Please select mode: \n1. Drive \n2. Turn \n3. Wait \n4. Start robot\n ") #Ask for mode
        if mode == "1":
            print("Drive mode selected")
            direction = input("Please select direction: \n1. Forward \n2. Backward \n") #Ask for direction
            if direction == "1":
                print("Please enter distance in centimeters: ")
                distance = input()
                print ("Stacking command to drive forward " + distance + " centimeters")
                self.datalist.append("A")
                self.datalist.extend(list(distance))
                #return self.datalist #Returns the command in the format "A" + distance
                return False
            elif direction == "2":
                print( "Please enter distance in centimeters: ")
                distance = input()
                print("Stacking command to drive backward " + distance + " centimeters")
                self.datalist.append("B")
                self.datalist.extend(list(distance))
                #return self.datalist #Returns the command in the format "B" + distance
                return False
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
                self.datalist.append("C")
                self.datalist.extend(list(degrees))
                #return self.datalist #Returns the command in the format "C" + degrees
                return False
            elif direction == "2":
                print("Please enter degrees to turn: ")
                degrees = input()
                print("Stacking command to turn left " + degrees + " degrees")
                self.datalist.append("D")
                self.datalist.extend(list(degrees))
                #return self.datalist #Returns the command in the format "D" + degrees
                return False
            else:
                print("Invalid input")
        if mode == "3":
            print("Wait mode selected")
            print("Please enter time in seconds: ")
            distance = input()
            print("Stacking command to wait for " + distance + " seconds")
            self.datalist.append("F")
            self.datalist.extend(list(distance))
            #return self.datalist #Returns the command in the format "F" + distance
            return False
        if mode == "4":
            print("Starting robot")
            self.datalist.append("E")
            #return self.datalist  #Returns the command "E" to send all commands
            return True

        
ui = UI() 
            
#UI().ui()