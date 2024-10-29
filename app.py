from flask import Flask, render_template, url_for, request, redirect, flash
from classes.Order import Order
from classes.Product import Product
from classes.OrderLine import OrderLine

app = Flask(__name__)
app.secret_key = 'secret_key' 

pizzas = [
    Product("Pepperoni", 10.0, ['Tomatoes, Garlic, Herbs, Mozzarella, Pepperoni'], ['gluten', 'milk'], 'images/pepperoni.jpeg'),
    Product("Margherita", 10.0, ['Tomatoes, Mozzarella, Fresh basil, Olive oil'], ['gluten', 'milk'], 'images/Margherita.jpeg'),
    Product("Neapolitan", 10.0, ['San Marzano tomatoes, Mozzarella di bufala, Fresh basil, Olive oil'], ['gluten', 'milk'], 'images/Neapolitan.jpeg'),
    Product("Romana", 10.0, ['Tomatoes, Mozzarella, Oregano, Anchovies (or other toppings)'], ['gluten', 'milk'], 'images/Romana.jpg')
]

fohOrderLineList = []

@app.route('/')
def index():
    return render_template('index.html', pizzas=pizzas)

@app.route('/order', methods=['POST'])
def order():
    pizza_name = request.form.get('pizza_name')
    selected_pizza = next((pizza for pizza in pizzas if pizza.name == pizza_name), None)
    
    if selected_pizza:
        pizza_price = selected_pizza.price
        pizza_image = selected_pizza.images
        return render_template('order.html', pizza_name=pizza_name, pizza_price=pizza_price, pizza_image=pizza_image)
    else:
        flash("Pizza not found!")
        return redirect(url_for('index'))
    
@app.route("/foh-create-order", methods=['POST', 'GET'])
def fohOrder():

    addedPizzaName = request.form.get("addedPizza")
    
    try:
        addedPizzaQuantity = int(request.form.get("addedQuantity"))
    except ValueError as a:
        print(f"ERROR: {a}")

    print(addedPizzaName)
    print(addedPizzaQuantity)
    
    selectedPizza = next((pizza for pizza in pizzas if pizza.name == addedPizzaName), None)

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

    # currently holding place holder values
    return render_template('fohOrderPage.html', completionCount = 4, tableNumber = 12, filteredProducts = pizzas, orderList = fohOrderLineList)



@app.route('/modify', methods=['POST'])
def modify():
    pizza_name = request.form.get('pizza_name')
    flash(f"You are modifying the {pizza_name} pizza!")
    return redirect(url_for('index'))

@app.routre('/fohOverview')
def fohOverview():
    return render_template('overveiw.html')

if __name__ == '__main__':
    app.run(debug=True)