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
//cart
// Initialize cart count
let cartCount = 0;

// Get cart count element
const cartCountDisplay = document.querySelector('.cart-count');

// Event listener for "Add to Cart" button
document.getElementById("addToCartBtn").addEventListener("click", function(event) {
    event.preventDefault();

    // Increment cart count
    cartCount++;
    cartCountDisplay.textContent = cartCount;

    // Get product details
    const selectedCapacity = document.getElementById('capacity').value;
    const selectedPrice = document.querySelector('.price-value').getAttribute("data-price");
    const customerName = document.getElementById('customer_name').value;

    // Total price calculation (assuming quantity is 1 for simplicity)
    const quantity = 1;
    const totalPrice = (parseFloat(selectedPrice) * quantity).toFixed(2);

    // Display message in modal
    modalMessage.innerHTML = `
        Customer Name: ${customerName}<br>
        Quantity: ${quantity}<br>
        Total Price: ${totalPrice} &euro;.
    `;
    modal.style.display = "block";
});

