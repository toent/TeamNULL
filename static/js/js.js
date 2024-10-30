// Initial animation trigger after 5 seconds
setTimeout(function() {
    document.getElementById('center-text').innerHTML = "<h1>Mario & Luigi's Pizzeria</h1>";
    document.getElementById('color-container').classList.add('move-up');
    document.getElementById('center-text').classList.add('move-text-up');
    setTimeout(function() {
        document.getElementById('boxes').classList.add('show-boxes');
    }, 1000);
}, 3000);

// Function to show the boxes on scroll if necessary
window.addEventListener('scroll', function() {
    const boxes = document.getElementById('boxes');
    const boxesPosition = boxes.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 1.5;

    if (boxesPosition < screenPosition) {
        boxes.classList.add('show-boxes');
    }
});

// Initialize cart count and load cart items from localStorage
let cartCount = 0;
const cartCountDisplay = document.querySelector('.cart-count');
const cartDetailsDisplay = document.querySelector('.cart-details');
let cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];

// Display the initial cart count and details if items exist
cartCount = cartItems.length;
cartCountDisplay.textContent = cartCount;
updateCartDetailsDisplay();

// Event listener for each ORDER button
document.querySelectorAll('.order-btn').forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default behavior

        // Get pizza details from button's data attributes
        const pizzaName = button.getAttribute('data-name');
        const pizzaPrice = parseFloat(button.getAttribute('data-price').replace('€', '').trim());
        const pizzaIngredients = button.getAttribute('data-ingredients');
        const pizzaAllergens = button.getAttribute('data-allergens');

        // Increment cart count and update display
        cartCount++;
        cartCountDisplay.textContent = cartCount;

        // Add item to cartItems array
        cartItems.push({
            name: pizzaName,
            price: pizzaPrice,
            ingredients: pizzaIngredients,
            allergens: pizzaAllergens
        });

        // Save updated cartItems to localStorage
        localStorage.setItem('cartItems', JSON.stringify(cartItems));
        updateCartDetailsDisplay(); // Update the cart details display
    });
});

// Function to update the cart details display
function updateCartDetailsDisplay() {
    if (cartItems.length === 0) {
        cartDetailsDisplay.innerHTML = '<p>Your cart is empty.</p>';
    } else {
        cartDetailsDisplay.innerHTML = cartItems.map(item => `
            <div class="cart-item">
                <strong>${item.name}</strong><br>
                <strong>Price: ${item.price} &euro;</strong><br>
            </div>
        `).join('');
    }
}
