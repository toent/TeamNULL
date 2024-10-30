from datetime import datetime

from flask import Flask, render_template, url_for, request, redirect, flash

from classes.Tags import Tags
from classes.DataManager import DataManager
from classes.Order import Order
from classes.OrderLine import OrderLine
from classes.Product import Product

app = Flask(__name__)
app.secret_key = 'secret_key'

dataManager = DataManager()

tags = Tags()

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
            Product("Romana", 10.0, ['Tomatoes, Mozzarella, Oregano, Anchovies (or other toppings)'],
                    ['gluten', 'milk'],
                    'images/Romana.jpg')
        ]
        dataManager.saveProducts()  # Save the products to the products.json file.

    # If there are no orders in the data manager, add some.
    if len(dataManager.orders) < 1:
        dataManager.orders = [
            Order([OrderLine(dataManager.products[0], 2)], 'Please don''t let Marcos cook it', 4),
            Order([OrderLine(dataManager.products[1], 1)], 'Please don''t let Marcos cook it', 5),
            Order([OrderLine(dataManager.products[2], 3)], 'Please don''t let Marcos cook it', 6),
            Order([OrderLine(dataManager.products[3], 4), OrderLine(dataManager.products[2], 2)], 'Please don''t let Marcos cook it', 7),
            Order([OrderLine(dataManager.products[2], 2), OrderLine(dataManager.products[1], 3)], 'Please don''t let Marcos cook it', 8),
        ]
        # Change the status of the orders.
        dataManager.orders[0].nextStatus()
        dataManager.orders[0].nextStatus()
        dataManager.orders[1].nextStatus()
        dataManager.orders[2].nextStatus()
        dataManager.saveOrders()  # Save the orders to the orders.json file.

    if len(tags.tagDict) < 1:
        tags.tagDict = {"tag-pizza": ["Margherita","Pepperoni","Neapolitan","Romana"], "tag-pasta":["Bolognese","Carbonara"], "tag-salad":["Caesar"], "tag-desert":["Gelato"], "tag-drinks":["Cola","Fanta","Sprite","Milkshake"],"tag-vegetarian":["Margherita","Neapolitan","Romana"], "tag-starter": ["Carpaccio", "Tomato Soup", "Mushroom Soup"]}
        tags.saveTags()


fohOrderLineList = []


@app.route('/')
def index():
    return render_template('index.html', pizzas=dataManager.products)


@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        # Get pizza details from form submission
        pizza_name = request.form.get('pizza_name')
        selected_pizza = next((pizza for pizza in dataManager.products if pizza.name == pizza_name), None)

        if selected_pizza:
            pizza_price = selected_pizza.price
            pizza_image = selected_pizza.images
            return render_template('order.html', pizza_name=pizza_name, pizza_price=pizza_price,
                                   pizza_image=pizza_image)
        else:
            flash("Pizza not found!")
            return redirect(url_for('index'))

    # Handle GET request for cart link navigation
    return render_template('order.html')


@app.route("/foh-create-order", methods=['POST', 'GET'])
def fohOrder():
    global tableNumber

    # Initialize variables from tag class    
    filteredProducts = list(dataManager.products)
    filterKeys = tags.tagKeys
    filterDict = tags.tagDict

    # Initialize variables from Forms
    currentTag = request.form.get("selectedTag")
    isOrderDone = bool(request.form.get("confirmOrder"))
    newTableNumber = request.form.get('tableNumber')
    addedPizzaName = request.form.get("addedPizza")
    addedPizzaQuantity = max(-1, int(request.form.get("addedQuantity", 0)))

    # Update the table number if provided
    if newTableNumber:
        tableNumber = newTableNumber

    # Debugging
    print(f"Table Number: {tableNumber}, Added Pizza: {addedPizzaName}, Added Quantity: {addedPizzaQuantity}")

    # Filter products if a valid tag is selected
    if currentTag and currentTag in filterKeys:
        # Create a new list with products that match the filter
        filteredProducts = [product for product in dataManager.products if product.name in filterDict[currentTag]]
    # If no valid tag is provided, filteredProducts will stay as all products by default
    print(filteredProducts)

    # Retrieve selected pizza
    selectedPizza = next((pizza for pizza in dataManager.products if pizza.name == addedPizzaName), None)

    # Finalize the order if it is done
    if isOrderDone and fohOrderLineList:
        newOrder = Order(fohOrderLineList, "Order from the Front of House", tableNumber)
        print(newOrder.toDict())
        dataManager.orders.append(newOrder)
        dataManager.saveOrders()
        fohOrderLineList.clear()
        return redirect(url_for("fohOverview"))  # Redirect to the overview page

    # Handle pizza addition to the order
    if selectedPizza and addedPizzaQuantity != 0:
        existingOrderLine = next((line for line in fohOrderLineList if line.product.name == selectedPizza.name), None)

        if existingOrderLine:
            existingOrderLine.quantity += addedPizzaQuantity
            if existingOrderLine.quantity <= 0:
                fohOrderLineList.remove(existingOrderLine)
        else:
            fohOrderLineList.append(OrderLine(selectedPizza, addedPizzaQuantity))

    # Calculate the total price
    priceTotal = sum(line.product.price * line.quantity for line in fohOrderLineList)

    # Render the template
    return render_template('fohOrderPage.html', priceTotal=priceTotal, tableNumber=tableNumber, filteredProducts=filteredProducts, orderList=fohOrderLineList)

@app.route('/modify', methods=['POST'])
def modify():
    pizza_name = request.form.get('pizza_name')
    flash(f"You are modifying the {pizza_name} pizza!")
    return redirect(url_for('index'))

# route for the FoH table overview page 
@app.route('/fohOverview', methods=['POST', 'GET'])
def fohOverview():
    return render_template('fohOverview.html', table1Status = "", table2Status = "", table3Status = "", table4Status = "", table5Status = "", table6Status = "", table7Status = "", table8Status = "", table9Status = "")


@app.route('/orderDisplay', methods=['GET'])
def orderDisplay():
    openOrders = [order for order in dataManager.orders if order.currentStatus == 'Submitted' or order.currentStatus == 'Ready']
    currentTime = datetime.now()
    return render_template('orderDisplay.html', openOrders=openOrders, currentTime=currentTime)


@app.route('/markDone', methods=['Post'])
def markDone():
    orderID = int(request.form.get('orderID'))
    order = next((order for order in dataManager.orders if order.orderID == orderID), None)
    if order:
        order.nextStatus()
        dataManager.saveOrders()
    return redirect(url_for('orderDisplay'))

if __name__ == '__main__':
    initialize()
    app.run(debug=True)
