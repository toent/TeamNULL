# This class represents a line in an order.
# Attributes:
# - product: Product - The product object that is being ordered from the class Product.
# - quantity: int - The quantity of the product that is being ordered.
from classes.Product import Product


class OrderLine:
    # region Constructors
    def __init__(self, product, quantity):
        """
        This class represents a line in an order.
        :param product: The product object that is being ordered from the class Product.
        :param quantity: The quantity of the product that is being ordered.
        """
        self.product = product
        self.quantity = quantity

    # endregion

    # region Methods
    def __str__(self):
        return f'{self.product} - {self.quantity}'

    def __repr__(self):
        return f'{self.product} - {self.quantity}'

    def toDict(self):
        return {
            'product': self.product.toDict(),
            'quantity': self.quantity
        }

    def fromDict(self, dict):
        self.product = Product('', 0, [], [])
        self.product.fromDict(dict['product'])
        self.quantity = dict['quantity']

    # endregion
