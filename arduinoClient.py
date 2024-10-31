import serial

from classes.Tags import Tags
from classes.DataManager import DataManager
from classes.Order import Order
from classes.OrderLine import OrderLine
from classes.Product import Product

dataManager = DataManager()

dataManagerLength = len(dataManager.orders)

freeTimers = [0,1,2,3]

redStatus = []
greenStatus = []
blueStatus = []
yellowStatus = []

# defining serial com port
arduino = serial.Serial('COM3',9600)

# function handling any serial inputs
def serialInputHandler():
    print("----- CHECKING FOR SERIAL INPUT -----")

    # check if serial buffer has any inputs present, and decoding them when present
    if arduino.in_waiting > 0:
        serialInput = arduino.readline().decode().strip()

        print("----- SERIAL INPUT FOUND -----")
        print("INPUT:",serialInput)
        print("------------------------------")

        # find the timer that became free and adding it to freeTimers
        if serialInput != "CONFIRM":
            freeTimers.append(serialInput)

            # wiping the respective status list for the now finished timer
            match (serialInput):
                case 0:
                    redStatus.clear()
                case 1:
                    greenStatus.clear()
                case 2:
                    blueStatus.clear()
                case 3:
                    yellowStatus.clear()
            return 0
        
        elif serialInput == "CONFIRM":
            return 1

# example of serial input
# "red"

# function to identify and send a cook request for the products of an input order
def productIdentifier(tempOrder):
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

            # looping until a free timer is found, and when found assigning the timer and storing the product info for that timer
            while len(productIdentifier) <= 3:
                print("----- CHECKING FOR TIMER -----")
                print("FREE IDs:",freeTimers)
                if len(freeTimers) > 0:
                    print("----- TIMER FOUND -----")
                    print("ID:",freeTimers[0])
                    print("-----------------------")

                    print("----- SENDING",freeTimers[0],"TO ARDUINO -----")
                    arduino.write(freeTimers[0])

                    match (freeTimers[0]):
                        case 0:
                            redStatus.extend(productIdentifier)
                            freeTimers.pop(0)
                            productIdentifier.append(0)
                        case 1:
                            greenStatus.extend(productIdentifier)
                            freeTimers.pop(0) 
                            productIdentifier.append(1)
                        case 2:
                            blueStatus.extend(productIdentifier)
                            freeTimers.pop(0)
                            productIdentifier.append(2)
                        case 3:                  
                            yellowStatus.extend(productIdentifier)
                            freeTimers.pop(0)
                            productIdentifier.append(3)

                serialConfirm = False

                while serialConfirm == False:
                    if serialInputHandler() == 1:
                        serialConfirm = True
                    else:
                        continue

                else:
                    print("----- NO TIMER FOUND -----")
                    # if there are no free timers, check for a free timer and try again
                    serialInputHandler()
                    continue

# for loop to check orders stored prior to code start for any submitted orders
for order in dataManager.orders:
    if order.currentStatus == "Submitted":
        print("----- EXISTING SUBMITTED ORDER FOUND -----")
        print("ORDER:",order)
        print("------------------------------------------")
        productIdentifier(order)
    else:
        continue

# while loop to handle orders created after code start
while True:
    if dataManagerLength < len(dataManager.orders):
        dataManagerLength = len(dataManager.orders)

        print("----- LATEST ORDER -----")
        print(dataManager.orders[dataManagerLength])
        print("------------------------")

        productIdentifier(dataManager.orders[dataManagerLength])