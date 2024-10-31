import os
from datetime import datetime

from flask import Flask, render_template, url_for, request, redirect, flash
from werkzeug.utils import secure_filename

from classes.Tags import Tags
from classes.DataManager import DataManager
from classes.Order import Order
from classes.OrderLine import OrderLine
from classes.Product import Product

imageUploadFolder = '/static/images'
allowedImageFiles = {'png', 'jpg', 'jpeg'}


app = Flask(__name__)
app.secret_key = 'secret_key'

dataManager = DataManager()

tags = Tags()
productTagRel = {}

fohOrderLineList = []

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

    # If there are no tags found, add some
    if len(tags.tagDict) < 1:
        tags.tagDict = {
            "tag-pizza": ["Margherita", "Pepperoni", "Neapolitan", "Romana"],   #these are all object tags which all will have their own icon in the foh order screen, therefore always leave them before the content tags
            "tag-pasta": ["Bolognese", "Carbonara"],
            "tag-salad": ["Caesar"],
            "tag-desert": ["Gelato"],
            "tag-drinks": ["Cola", "Fanta", "Sprite", "Milkshake"],
            "tag-starter": ["Carpaccio", "Tomato Soup", "Mushroom Soup"],
            "tag-vegetarian": ["Margherita", "Neapolitan", "Romana"]            #the content tags start from here (vegetarian)
        }
        tags.saveTags()

    # Setup relations between products and tags

    setupTagRels()

    print(productTagRel)

def setupTagRels():
    for product in dataManager.products:
        productTagRel[product.name] = []
        for tag, product_list in tags.tagDict.items():
            if product.name in product_list:
                productTagRel[product.name].append(tag)
    return productTagRel

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
            # Get the quantity from the form (default to 1 if not provided)
            quantity = request.form.get('quantity', 1, type=int)

            # Pass all necessary data to the order_summary template
            return render_template('order.html', 
                                   pizza_name=pizza_name, 
                                   pizza_price=pizza_price, 
                                   quantity=quantity, 
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
    return render_template('fohOrderPage.html', priceTotal=priceTotal, tableNumber=tableNumber, filteredProducts=filteredProducts, orderList=fohOrderLineList, selectButtonClass=productTagRel)

@app.route('/modify', methods=['POST'])
def modify():
    pizza_name = request.form.get('pizza_name')
    flash(f"You are modifying the {pizza_name} pizza!")
    return redirect(url_for('index'))

def tableStatusCheck(tempTableStatus,tempOrder):
    if tempOrder.currentStatus == "Ready":
        tempTableStatus = "Ready"
    elif tempOrder.currentStatus == "Submitted" and tempTableStatus != "Ready":
        tempTableStatus = "Submitted"
    elif tempTableStatus != "Ready" and tempTableStatus != "Submitted":
        tempTableStatus = "Finished"
    
    return tempTableStatus

# route for the FoH table overview page 
@app.route('/fohOverview', methods=['POST', 'GET'])
def fohOverview():
    table1Status = "Finished"
    table2Status = "Finished"
    table3Status = "Finished"
    table4Status = "Finished"
    table5Status = "Finished"
    table6Status = "Finished"
    table7Status = "Finished"
    table8Status = "Finished"
    table9Status = "Finished"

    for order in dataManager.orders:
        match int(order.table):
            case 1:
                table1Status = tableStatusCheck(table1Status,order)
            case 2:
                table2Status = tableStatusCheck(table2Status,order)
            case 3:
                table3Status = tableStatusCheck(table3Status,order)
            case 4:
                table4Status = tableStatusCheck(table4Status,order)
            case 5:
                table5Status = tableStatusCheck(table5Status,order)
            case 6:
                table6Status = tableStatusCheck(table6Status,order)
            case 7:
                table7Status = tableStatusCheck(table7Status,order)
            case 8:
                table8Status = tableStatusCheck(table8Status,order)
            case 9:
                table9Status = tableStatusCheck(table9Status,order)

    return render_template('fohOverview.html', table1Status = table1Status, table2Status = table2Status, table3Status = table3Status, table4Status = table4Status, table5Status = table5Status, table6Status = table6Status, table7Status = table7Status, table8Status = table8Status, table9Status = table9Status)


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

@app.route('/manageproducts', methods=['POST', 'GET'])
def manageProduct():
    processedIngredients = []
    processedAllergens = []
    sourceProductDict = {}
    
    selectedProduct = request.form.get('selectedProduct')
    print(f"Selected Product: {selectedProduct}")

    if selectedProduct != (None or "NewProduct"):
        for product in dataManager.products:
            if product.name == selectedProduct:
                 sourceProductDict = product
    else:
        sourceProductDict = {"name": "NewProduct", "price": 0.00, "ingredients": "", "allergens": "", "images": "images/"}
           

    productName = request.form.get('productName')
    productPrice = request.form.get('productPrice')
    productIngredients = request.form.get('productIngredients')
    productAllergens = request.form.get('productAllergens')
    productImageName = request.form.get('productImage')
    productImage = request.files['productImage']

    # convert ingredients and allergens into proper format
    if productIngredients:
        processedIngredients = productIngredients.removeprefix("['").removesuffix("']").split(", ")
        for i in range(len(processedIngredients)):
            processedIngredients[i] = processedIngredients[i].capitalize()

    if productAllergens:
        processedAllergens = productAllergens.removeprefix("['").removesuffix("']").split("', '")
        for i in range(len(processedAllergens)):
            processedAllergens[i] = processedAllergens[i].capitalize()

    # DEBUGGING
    print(f"Product Name: {productName}")
    print(f"Product Price: {productPrice}")
    print(f"Product Ingredients:{productIngredients}")
    print(f"Processed Ingredients: {processedIngredients}")
    print(f"Product Allergens:{productAllergens}")
    print(f"Processed Allergens: {processedAllergens}")
    print(f"Product Image: {productImageName}")

    if productImage and allowedImage(productImageName):
        imageFileName = secure_filename(productImageName)
        productImage.save(os.path.join(imageUploadFolder, imageFileName))

    return render_template('productManagement.html', productList=dataManager.products, tagList=tags.tagKeys, productEdit = sourceProductDict)

def allowedImage(imageFileName):
    return '.' in imageFileName and imageFileName.rsplit('.', 1)[1].lower() in allowedImageFiles

if __name__ == '__main__':
    initialize()
    app.run(debug=True)
