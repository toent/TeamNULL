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
