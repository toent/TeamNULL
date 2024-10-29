from flask import Flask, render_template, url_for, request, redirect, flash

from classes.DataManager import DataManager
from classes.Order import Order
from classes.OrderLine import OrderLine
from classes.Product import Product

app = Flask(__name__)
app.secret_key = 'secret_key'

dataManager = DataManager()

tableNumber = 1

def initialize():
    """
    This method will initialize the application. It currently has a hardcoded dataset for testing purposes.
    """
    # If there are no products in the data manager, add some.
    if len(dataManager.products) < 1:
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
        dataManager.saveProducts() # Save the products to the products.json file.

    # If there are no orders in the data manager, add some.
    if len(dataManager.orders) < 1:
        dataManager.orders = [
            Order([OrderLine(dataManager.products[0], 2)], 'Please don''t let Marcos cook it', 4),
            Order([OrderLine(dataManager.products[1], 1)], 'Please don''t let Marcos cook it', 5),
            Order([OrderLine(dataManager.products[2], 3)], 'Please don''t let Marcos cook it', 6),
            Order([OrderLine(dataManager.products[3], 4)], 'Please don''t let Marcos cook it', 7)
        ]
        # Change the status of the orders.
        dataManager.orders[0].nextStatus()
        dataManager.orders[0].nextStatus()
        dataManager.orders[1].nextStatus()
        dataManager.orders[2].nextStatus()
        dataManager.saveOrders() # Save the orders to the orders.json file.

fohOrderLineList = []


@app.route('/')
def index():
    return render_template('index.html', pizzas=dataManager.products)


@app.route('/order', methods=['POST'])
def order():
    pizza_name = request.form.get('pizza_name')
    selected_pizza = next((pizza for pizza in dataManager.products if pizza.name == pizza_name), None)

    if selected_pizza:
        pizza_price = selected_pizza.price
        pizza_image = selected_pizza.images
        return render_template('order.html', pizza_name=pizza_name, pizza_price=pizza_price, pizza_image=pizza_image)
    else:
        flash("Pizza not found!")
        return redirect(url_for('index'))


@app.route("/foh-create-order", methods=['POST', 'GET'])
def fohOrder():
    priceTotal = 0

    addedPizzaName = request.form.get("addedPizza")

    try:
        tableNumber = request.form.get('tableNumber')
    except:
        tableNumber = 1

    try:
        addedPizzaQuantity = int(request.form.get("addedQuantity"))
    except:
        addedPizzaQuantity = 0

    print(addedPizzaName)
    print(addedPizzaQuantity)

    selectedPizza = next((pizza for pizza in dataManager.products if pizza.name == addedPizzaName), None)

    if selectedPizza:
        existingOrderLine = next((line for line in fohOrderLineList if line.product.name == selectedPizza.name), None)
        if existingOrderLine:
            new_quantity = existingOrderLine.quantity + addedPizzaQuantity
            if new_quantity > 0:
                existingOrderLine.quantity = new_quantity
            else:
                fohOrderLineList.remove(existingOrderLine)
        else:
            if addedPizzaQuantity > 0:
                createdOrderline = OrderLine(selectedPizza, addedPizzaQuantity)
                fohOrderLineList.append(createdOrderline)

    if(len(fohOrderLineList) > 0):
        for product in fohOrderLineList:
            priceTotal += product.product.price * product.quantity
    else:
        priceTotal = 0

    # currently holding place holder values
    return render_template('fohOrderPage.html', priceTotal=priceTotal , tableNumber=tableNumber, filteredProducts=dataManager.products,
                           orderList=fohOrderLineList)


@app.route('/modify', methods=['POST'])
def modify():
    pizza_name = request.form.get('pizza_name')
    flash(f"You are modifying the {pizza_name} pizza!")
    return redirect(url_for('index'))

@app.route('/fohOverview')
def fohOverview():
    tableNumber = request.form.get('tableNumber')

    return render_template('overview.html')

if __name__ == '__main__':
    initialize()
    app.run(debug=True)
