from flask import Flask, render_template, url_for, request, redirect, flash
from classes.Order import Order
from classes.Product import Product
from classes.OrderLine import OrderLine

app = Flask(__name__)
app.secret_key = 'secret_key' 

pizzas = [
    {
        'name': 'Pepperoni',
        'description': 'Tomatoes, Garlic, Herbs, Mozzarella, Pepperoni',
        'price': 10,
        'image': 'images/pepperoni.jpeg',
        'allergens': ['gluten', 'milk']
    },
    {
        'name': 'Margherita',
        'description': 'Tomatoes, Mozzarella, Fresh basil, Olive oil',
        'price': 10,
        'image': 'images/Margherita.jpeg',
        'allergens': ['gluten', 'milk']
    },
    {
        'name': 'Neapolitan',
        'description': 'San Marzano tomatoes, Mozzarella di bufala, Fresh basil, Olive oil',
        'price': 10,
        'image': 'images/Neapolitan.jpeg',
        'allergens': ['gluten', 'milk']
    },
    {
        'name': 'Romana',
        'description': 'Tomatoes, Mozzarella, Oregano, Anchovies (or other toppings)',
        'price': 10,
        'image': 'images/Romana.jpg',
        'allergens': ['gluten', 'milk']
    }
]

fohOrderLineList = []

@app.route('/')
def index():
    return render_template('index.html', pizzas=pizzas)

@app.route('/order', methods=['POST'])
def order():
    pizza_name = request.form.get('pizza_name')
    selected_pizza = next((pizza for pizza in pizzas if pizza['name'] == pizza_name), None)
    
    if selected_pizza:
        pizza_price = selected_pizza['price']
        pizza_image = selected_pizza['image']
        return render_template('order.html', pizza_name=pizza_name, pizza_price=pizza_price, pizza_image=pizza_image)
    else:
        flash("Pizza not found!")
        return redirect(url_for('index'))
    
@app.route("/foh-create-order", methods=['POST', 'GET'])
def fohOrder():

    
    try:
        addedPizzaName = request.form.get("addedPizza")
        addedPizzaQuantity = request.form.get("addedQuantity")
        print(addedPizzaQuantity)
        selectedPizza = next((pizza for pizza in pizzas if pizza['name'] == addedPizzaName), None)

        if(selectedPizza != None and addedPizzaQuantity != None):

            createdProduct = Product(selectedPizza['name'], selectedPizza['price'], selectedPizza['description'], selectedPizza['allergens'])
            createdOrderline = OrderLine(createdProduct, addedPizzaQuantity)

            if (len(fohOrderLineList) > 0):
                lineCount = 0
                for line in fohOrderLineList:
                    if (line.product == createdOrderline.product and lineCount == 0):
                        line.quantity += 1
                        lineCount += 1
                        print("Added Extra")
                        print(len(fohOrderLineList))
                        print(fohOrderLineList)

                if(lineCount == 0):
                    fohOrderLineList.append(createdOrderline)    
                    lineCount += 1   
                    print("Added New") 
                    print(len(fohOrderLineList))
                    print(fohOrderLineList)
            else:
                fohOrderLineList.append(createdOrderline)       
                print("Added New") 
                print(len(fohOrderLineList))
                print(fohOrderLineList)
            
            # if(fohOrderLineList.index(selectedPizza['name']) == ValueError):
            #     if(addedPizzaQuantity > 0):
            #         print(createdOrderline)
            #         fohOrderLineList.append(createdOrderline)
            #         print(fohOrderLineList)   
            #     else:
            #         print("REMOVING")
            #         fohOrderLineList.remove(createdOrderline)
            # else:
            #     try:
            #         pizzaIndex = fohOrderLineList.index(selectedPizza)
            #         fohOrderLineList[pizzaIndex].quantity = fohOrderLineList[pizzaIndex].quantity + 1
            #     except ValueError as a:
            #         print(a)
    except ValueError as b:
        print(f"failed {b}")
        fohOrderLineList.clear()



    print(addedPizzaName)
    # currently holding place holder values
    return render_template('fohOrderPage.html', completionCount = 4, tableNumber = 12, filteredProducts = pizzas, orderList = fohOrderLineList)


@app.route('/modify', methods=['POST'])
def modify():
    pizza_name = request.form.get('pizza_name')
    flash(f"You are modifying the {pizza_name} pizza!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)