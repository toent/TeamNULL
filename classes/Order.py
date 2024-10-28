from datetime import datetime
from random import Random


# This class represents an order.
# Attributes:
# - orderID: int - The ID of the order.
# - products: list - A list of OrderLine objects that represent the products being ordered.
# - timeCreated: datetime - The date and time when the order was created.
# - timeFinished: datetime - The date and time when the order was finished.
# - currentStatus: str - The current status of the order. It can be 'Submitted', 'In Progress' or 'Finished'.
# - notes: str - Any notes that the customer might have.
class Order:

    # region Constructors
    def __init__(self, products, notes):
        """
        This class represents an order.
        :param products: A list of OrderLine objects that represent the products being ordered.
        :param notes: A string with any notes that the customer might have.
        """
        self.orderID = Random().randint(1000, 9999)
        self.products = products
        self.timeCreated = datetime.now()
        self.timeFinished = None
        self.currentStatus = 'Submitted'
        self.notes = notes

    # endregion

    # region Methods
    def __str__(self):
        return f'{self.orderID} - {self.currentStatus}'

    def __repr__(self):
        return f'{self.orderID} - {self.currentStatus}'

    def nextStatus(self):
        """
        This method will change the status of the order to the next one.
        If the order is already finished, it will raise a ValueError exception.
        """
        if self.currentStatus == 'Submitted':
            self.currentStatus = 'In Progress'
        elif self.currentStatus == 'In Progress':
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

    # endregion
