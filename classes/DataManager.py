import json
from classes.Order import Order
from classes.Product import Product


# This class is responsible for managing the data of the application and storing it in json files.
# It has the following attributes:
# - orders: list - A list of Order objects.
# - products: list - A list of Product objects.
class DataManager:
    # region Constructors
    def __init__(self):
        self.orderFile = 'storage/orders.json'
        self.productFile = 'storage/products.json'
        self.orders = []
        self.products = []
        self.loadProducts()
        self.loadOrders()

    # endregion

    # region Methods
    def loadOrders(self):
        """
        This method will load the orders from the orders.json file.
        """
        try:
            with open(self.orderFile, 'r') as file:
                orders = json.load(file)
                for order in orders:
                    newOrder = Order([], '', 0)
                    newOrder.fromDict(order)
                    self.orders.append(newOrder)
        except FileNotFoundError:
            print('Data Manager: Could not load orders. File not found')

    def saveOrders(self):
        """
        Checks if file exists, if not, creates it.
        This method will save the orders to the orders.json file.
        """
        with open(self.orderFile, 'w') as file:
            json.dump([order.toDict() for order in self.orders], file)

    def loadProducts(self):
        """
        This method will load the products from the products.json file.
        """
        try:
            with open(self.productFile, 'r') as file:
                products = json.load(file)
                for prod in products:
                    product = Product("", 0, [], [], [])
                    product.fromDict(prod)
                    self.products.append(product)
        except FileNotFoundError:
            print('Data Manager: Could not load products. File not found')

    def saveProducts(self):
        """
        This method will save the products to the products.json file.
        """
        with open(self.productFile, 'w') as file:
            json.dump([product.toDict() for product in self.products], file)

    def availableID(self):
        """
        This method will return the first available ID for an order.
        """
        return max([order['orderID'] for order in self.orders], default=0) + 1

    # endregion
