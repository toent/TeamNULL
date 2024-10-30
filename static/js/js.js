// Initial animation trigger after 5 seconds
setTimeout(function() {
    // Update the center text
    document.getElementById('center-text').innerHTML = "<h1>Mario & Luigi's Pizzeria</h1>";

    // Animate the flag and text moving upwards
    document.getElementById('color-container').classList.add('move-up');
    document.getElementById('center-text').classList.add('move-text-up');

    // Show the boxes after 1 second (after the animation completes)
    setTimeout(function() {
        document.getElementById('boxes').classList.add('show-boxes');
    }, 1000);

}, 3000);  // 3000 milliseconds = 5 seconds delay

// Function to show the boxes on scroll if necessary
window.addEventListener('scroll', function() {
    const boxes = document.getElementById('boxes');
    const boxesPosition = boxes.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 1.5;

    if (boxesPosition < screenPosition) {
        boxes.classList.add('show-boxes');
    }
});

// Initialize cart count
let cartCount = 0;

// Get cart count and cart details elements
const cartCountDisplay = document.querySelector('.cart-count');
const cartDetailsDisplay = document.querySelector('.cart-details');

// Event listener for cart image to navigate to the order page
document.querySelector('.cart img').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent default link behavior
    window.location.href = orderUrl; // Use the pre-defined order URL
});

// Attach event listeners to each "Order" button
document.querySelectorAll('.order-btn').forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent form submission

        // Increment cart count
        cartCount++;
        cartCountDisplay.textContent = cartCount;

        // Get pizza details from form inputs
        const form = event.target.closest('form');
        const pizzaName = form.querySelector('input[name="pizza_name"]').value;
        const pizzaPrice = form.closest('.pizza-info').querySelector('.details span:last-child').textContent;

        // Update cart details
        cartDetailsDisplay.innerHTML += `
            <div class="cart-item">
                <strong>${pizzaName}</strong><br>
                <strong>${pizzaPrice}</strong>
            </div>
        `;
    });
});
