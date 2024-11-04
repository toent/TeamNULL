import os
import time
from enum import unique
import serial

from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from werkzeug.utils import secure_filename

from classes.Tags import Tags
from classes.DataManager import DataManager
from classes.Order import Order
from classes.OrderLine import OrderLine
from classes.Product import Product

# defining serial com port
ser = serial.Serial(port="COM3",baudrate=115200,timeout=1)

handshake = "9999"
handshakeVerify = ser.write(bytes(handshake,"utf-8"))
print("----- HANDSHAKE:",handshakeVerify,"-----")
time.sleep(1)

dataManager = DataManager()

dataManagerLength = len(dataManager.orders) - 1

freeTimers = [1,2,3,4]

redStatus = []
greenStatus = []
blueStatus = []
yellowStatus = []

# function handling any serial inputs
def serialInputHandler(timerToConfirm):
    print("----- CHECKING FOR SERIAL INPUT -----")

    # check if serial buffer has any inputs present, and decoding them when present
    if ser.in_waiting > 0:
        serialInput = int(ser.readline().decode("utf-8"))
        time.sleep(1)

        print("----- SERIAL INPUT FOUND -----")
        print("Input:",serialInput)
        print("------------------------------")

        # find the timer that became free and adding it to freeTimers
        if int(serialInput) <= 4:
            print("----- COMPLETED TIMER",serialInput,"REGISTERED -----")
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
        
        elif serialInput == (timerToConfirm):
            print("----- INPUT CONFIRMATION FOUND -----")
            print("A Type:",type(serialInput),"A Data:",serialInput)
            print("B Type:",type(timerToConfirm),"B Data:",timerToConfirm)
            print("------------------------------------")
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
        for x in range(0,(product.quantity)):
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
                print("# OF TIMERS:",len(freeTimers))
                if len(freeTimers) == 0:
                    print("----- NO TIMER FOUND -----")
                    # if there are no free timers, check for a free timer and try again
                    serialInputHandler(9)
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
                ser.write(bytes(sendData,"utf-8"))
                time.sleep(1)

                # checking for confirmation from the arduino of an assigned timer
                if serialInputHandler(freeTimers[0] + 4) == 1:
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

print("----- EXISTING ORDERS COMPLETE -----")

# while loop to handle orders created after code start
while True:
    print("----- CHECKING FOR NEW ORDERS -----")
    dataManager.loadOrders()

    if dataManagerLength < len(dataManager.orders) - 1:
        print("----- NEW ORDERS DETECTED -----")
        dataManagerPreviousLength = dataManagerLength
        dataManagerLength = len(dataManager.orders) - 1

        for x in range(dataManagerPreviousLength,dataManagerLength):
            tempOrder = dataManager.orders[x]
            
            print("----- ORDER FOUND -----")
            print("ORDER:",tempOrder)
            print("------------------------------------------")
            productTimerManager(tempOrder)

    time.sleep(5)