from serial import Serial

from classes.Tags import Tags
from classes.DataManager import DataManager
from classes.Order import Order
from classes.OrderLine import OrderLine
from classes.Product import Product

dataManager = DataManager()

dataManagerLength = len(dataManager.orders)

freeTimers = [1,2,3,4]

redStatus = []
greenStatus = []
blueStatus = []
yellowStatus = []

# defining serial com port
ser = Serial(port='COM3',baudrate='9600')

# function handling any serial inputs
def serialInputHandler(timerToConfirm):
    print("----- CHECKING FOR SERIAL INPUT -----")

    # check if serial buffer has any inputs present, and decoding them when present
    if ser.in_waiting > 0:
        serialInput = ser.readline().decode("utf-8")

        print("----- SERIAL INPUT FOUND -----")
        print("INPUT:",serialInput)
        print("------------------------------")

        # find the timer that became free and adding it to freeTimers
        if int(serialInput) > 4:
            freeTimers.append(serialInput)

            # wiping the respective status list for the now finished timer
            match (serialInput):
                case 1:
                    redStatus.clear()
                case 2:
                    greenStatus.clear()
                case 3:
                    blueStatus.clear()
                case 4:
                    yellowStatus.clear()
            return 0
        
        elif serialInput == (str(timerToConfirm + 4)):
            return 1

# function to identify and send a cook request for the products of an input order
def productTimerManager(tempOrder):
    # store the tempOrder's id for product tracking
    tempOrderId = tempOrder.orderID

    print("----- STORED ID FOR ORDER -----")
    print("ORDER ID",tempOrderId)
    print("-------------------------------")

    # find the quanitity of a product in the order
    for product in tempOrder.products:
        for x in range(1,(product.quantity)):
            # create a temporary list to make product identifier strings containing:
            # tempOrder id, product name, # (out of total # of that product name in the order)
            productIdentifier = []
            
            productIdentifier.append(str(tempOrderId))
            productIdentifier.append(str(product.product.name))
            productIdentifier.append(str(x))

            print("----- PRODUCT IDENTIFIED -----")
            print(productIdentifier)
            print("------------------------------")

            timerFound = False
            # looping until a free timer is found, and when found assigning the timer and storing the product info for that timer
            while timerFound == False :
                print("----- CHECKING FOR TIMER -----")
                print("FREE IDs:",freeTimers)
                if len(freeTimers) < 0:
                    print("----- NO TIMER FOUND -----")
                    # if there are no free timers, check for a free timer and try again
                    serialInputHandler()
                    continue

                else:
                    print("----- TIMER FOUND -----")
                    print("ID:",freeTimers[0])
                    print("-----------------------")

                    sendData = str(freeTimers[0])

                    timerFound = True

            serialConfirm = False
            while serialConfirm == False:
                # sending serial request
                print("----- SENDING",sendData,"TO ARDUINO -----")
                ser.write(sendData.encode())

                # checking for confirmation from the arduino of an assigned timer
                if serialInputHandler(freeTimers[0]) == 1:
                    print("----- TIMER ASSIGNMENT CONFIRMATION RECIEVED -----")
                    # adding the status to the selected timer, removing the timer from freeTimers
                    match (freeTimers[0]):
                        case 1:
                            redStatus.extend(productIdentifier)
                            freeTimers.pop(0)
                            print("----- MOVINGTO NEXT PRODUCT -----")
                        case 2:
                            greenStatus.extend(productIdentifier)
                            freeTimers.pop(0) 
                            print("----- MOVINGTO NEXT PRODUCT -----")
                        case 3:
                            blueStatus.extend(productIdentifier)
                            freeTimers.pop(0)
                            print("----- MOVINGTO NEXT PRODUCT -----")
                        case 4:                  
                            yellowStatus.extend(productIdentifier)
                            freeTimers.pop(0)
                            print("----- MOVINGTO NEXT PRODUCT -----")  
                    
                    # breaking the loop
                    serialConfirm = True

                else:
                    # trying again if no confirmation is recieved
                    print("----- AWAITING TIMER ASSIGNEMENT CONFRIMATION -----")
                    continue

# for loop to check orders stored prior to code start for any submitted orders
for order in dataManager.orders:
    if order.currentStatus == "Submitted":
        print("----- EXISTING SUBMITTED ORDER FOUND -----")
        print("ORDER:",order)
        print("------------------------------------------")
        productTimerManager(order)
    else:
        continue

# while loop to handle orders created after code start
while True:
    if dataManagerLength < len(dataManager.orders):
        dataManagerLength = len(dataManager.orders)

        print("----- LATEST ORDER -----")
        print(dataManager.orders[dataManagerLength])
        print("------------------------")

        productTimerManager(dataManager.orders[dataManagerLength])