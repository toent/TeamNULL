
@app.route('/order', methods=['POST'])
def order():
    pizza_name = request.form.get('pizza_name')
    flash(f"You ordered a {pizza_name} pizza!")
    return redirect(url_for('index'))