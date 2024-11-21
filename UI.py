def ui():
    print("Welcome to the Robot Control System")
    
    #Ask for mode
    mode = input("Please select mode: \n1. Drive \n2. Turn \n3. Send commands\n")
    
    if mode == "1":
        print("Drive mode selected")
        #Ask for direction
        direction = input("Please select direction: \n1. Forward \n2. Backward \n")
        
        if direction == "1":
            print("Please enter distance in meters: ")
            distance = input()
            print ("Driving forward " + distance + " meters")
            
        elif direction == "2":
            print( "Please enter distance in meters: ")
            distance = input()
            print("Driving backward " + distance + " meters")
        else:
            print("Invalid input")
            
    if mode == "2":
        print("Turn mode selected")
        #Ask for direction
        direction = input("Please select direction: \n1. Right \n2. Left \n")
        
        if direction == "1":
            print("Please enter degrees to turn: ")
            degrees = input()
            print("Turning right " + degrees + " degrees")
        elif direction == "2":
            print("Please enter degrees to turn: ")
            degrees = input()
            print("Turning left " + degrees + " degrees")
        else:
            print("Invalid input")
            
    if mode == "3":
        print("Sending all commands")
ui()