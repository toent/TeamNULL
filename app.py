from flask import Flask, render_template, url_for, request, redirect, flash

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


@app.route('/modify', methods=['POST'])
def modify():
    pizza_name = request.form.get('pizza_name')
    flash(f"You are modifying the {pizza_name} pizza!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)