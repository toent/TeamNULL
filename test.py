from classes.DataManager import DataManager
from classes.Order import Order
from classes.OrderLine import OrderLine
from classes.Product import Product

#TESTING FOR DATA MANAGER
dataManager = DataManager()

products = []
orders = []

def initializeDataset():
    dataManager.products = [
        Product("Pepperoni", 10.0, ['Tomatoes, Garlic, Herbs, Mozzarella, Pepperoni'], ['gluten', 'milk'],
                'images/pepperoni.jpeg'),
        Product("Margherita", 10.0, ['Tomatoes, Mozzarella, Fresh basil, Olive oil'], ['gluten', 'milk'],
                'images/Margherita.jpeg'),
        Product("Neapolitan", 10.0, ['San Marzano tomatoes, Mozzarella di bufala, Fresh basil, Olive oil'],
                ['gluten', 'milk'], 'images/Neapolitan.jpeg'),
        Product("Romana", 10.0, ['Tomatoes, Mozzarella, Oregano, Anchovies (or other toppings)'], ['gluten', 'milk'],
                'images/Romana.jpg')
    ]
    dataManager.orders = [
        Order([OrderLine(dataManager.products[0], 2)], 'Please don''t let Marcos cook it', 4),
        Order([OrderLine(dataManager.products[1], 1)], 'Please don''t let Marcos cook it', 5),
        Order([OrderLine(dataManager.products[2], 3)], 'Please don''t let Marcos cook it', 6),
        Order([OrderLine(dataManager.products[3], 4)], 'Please don''t let Marcos cook it', 7)
    ]

def testSaveProducts():
    try:
        dataManager.saveProducts()
        print("saveProducts() test passed")
    except:
        print("saveProducts() test failed")

def testLoadProducts():
    try:
        dataManager.loadProducts()
        print("loadProducts() test passed")
    except:
        print("loadProducts() test failed")

def testSaveOrders():
    try:
        dataManager.saveOrders()
        print("saveOrders() test passed")
    except:
        print("saveOrders() test failed")

def testLoadOrders():
    try:
        dataManager.loadOrders()
        print("loadOrders() test passed")
    except:
        print("loadOrders() test failed")

initializeDataset()
testSaveProducts()
testLoadProducts()
testSaveOrders()
testLoadOrders()
