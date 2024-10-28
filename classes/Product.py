# This class represents a product.
# Attributes:
# - name: str - The name of the product.
# - price: float - The price of the product.
# - ingredients: list - A list of strings with the ingredients of the product.
# - allergens: list - A list of strings with the allergens of the product.
class Product:

    # region Constructors
    def __init__(self, name, price, ingredients, allergens):
        self.name = name
        self.price = price
        self.ingredients = ingredients
        self.allergens = allergens

    # endregion

    # region Methods
    def __str__(self):
        return f'{self.name} - {self.price}'

    def __repr__(self):
        return f'{self.name} - {self.price}'
    # endregion