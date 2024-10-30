from datetime import datetime
from random import Random

from classes.OrderLine import OrderLine
from classes.Product import Product


# This class represents an order.
# Attributes:
# - orderID: int - The ID of the order.
# - products: list - A list of OrderLine objects that represent the products being ordered.
# - timeCreated: datetime - The date and time when the order was created.
# - timeFinished: datetime - The date and time when the order was ready.
# - currentStatus: str - The current status of the order. It can be 'Submitted', 'Ready' or 'Finished'.
# - notes: str - Any notes that the customer might have.
class Order:

    # region Constructors
    def __init__(self, products, notes, table):
        """
        This class represents an order.
        :param products: A list of OrderLine objects that represent the products being ordered.
        :param notes: A string with any notes that the customer might have.
        """
        self.orderID = Random().randint(10000000, 99999999)
        self.products = products
        self.timeCreated = datetime.now()
        self.timeFinished = 0
        self.currentStatus = 'Submitted'
        self.notes = notes
        self.table = table

    # endregion

    # region Methods
    def __str__(self):
        """
        This method will return a string representation of the order with all of the order information.
        :return:
        """
        return f'Order ID: {self.orderID}\n Products: {self.products}\n Time Created: {self.timeCreated}\n Time Finished: {self.timeFinished}\n {self.table}\n Current Status: {self.currentStatus}\n Notes: {self.notes}'

    def __repr__(self):
        return f'{self.orderID} - {self.currentStatus}'

    def nextStatus(self):
        """
        This method will change the status of the order to the next one.
        If the order is already delivered, it will raise a ValueError exception.
        """
        if self.currentStatus == 'Submitted':
            self.currentStatus = 'Ready'
        elif self.currentStatus == 'Ready':
            self.currentStatus = 'Finished'
            self.timeFinished = datetime.now()
        else:
            raise ValueError('Order is already finished')

    def isOrderFinished(self):
        """
        This method will return True if the order is finished, False otherwise.
        :return: bool - True if the order is finished, False otherwise.
        """
        return self.currentStatus == 'Finished'

    def toDict(self):
        return {
            'orderID': self.orderID,
            'products': [product.toDict() for product in self.products],
            'timeCreated': self.timeCreated.strftime('%Y-%m-%d %H:%M:%S'),
            'timeFinished': self.timeFinished.strftime('%Y-%m-%d %H:%M:%S') if self.timeFinished else 0,
            'currentStatus': self.currentStatus,
            'notes': self.notes,
            'table': self.table
        }

    def fromDict(self, dict):
        self.orderID = dict['orderID']
        self.products = [OrderLine(Product('', 0, [],[], []), 0).fromDict(product) for product in dict['products']]
        self.timeCreated = datetime.strptime(dict['timeCreated'], '%Y-%m-%d %H:%M:%S')
        self.timeFinished = datetime.strptime(dict['timeFinished'], '%Y-%m-%d %H:%M:%S') if dict['timeFinished'] else None
        self.currentStatus = dict['currentStatus']
        self.notes = dict['notes']
        self.table = dict['table']

    # endregion
