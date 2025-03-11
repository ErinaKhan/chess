import time

def chooseTime():
    print("10, 5 or 3")  # Show options before asking
    timeChoice = input("What time set would you like to play? ")
    
    if timeChoice == "10":
        timer10()  # Fixed function name
    elif timeChoice == "5":
        timer5()
    elif timeChoice == "3":
        timer3()
    else:
        print("Invalid choice!")

def timer10():
    t = 600  # 10 minutes in seconds
    while t > 0:
        print(t, "seconds left")
        time.sleep(1)
        t -= 1
    print("Time's up!")

def timer5():
    t = 300  # 5 minutes in seconds
    while t > 0:
        print(t, "seconds left")
        time.sleep(1)
        t -= 1
    print("Time's up!")

def timer3():
    t = 180  # 3 minutes in seconds
    while t > 0:
        print(t, "seconds left")
        time.sleep(1)
        t -= 1
    print("Time's up!")

# Call the function to start
chooseTime()
