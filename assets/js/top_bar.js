document.addEventListener("DOMContentLoaded", function() {
    const messages = document.querySelectorAll('.top-message');
    let currentMessageIndex = 0;

    // Function to show one message at a time
    function showNextMessage() {
        // Hide all messages
        messages.forEach(message => {
            message.style.display = 'none';
        });

        // Show the current message
        messages[currentMessageIndex].style.display = 'block';

        // Move to the next message or loop back to the first
        currentMessageIndex = (currentMessageIndex + 1) % messages.length;

        // Set a timeout to show the next message
        setTimeout(showNextMessage, 10000); // Change 5000 to the desired interval in milliseconds
    }

    if (messages.length > 0) {
        showNextMessage(); // Start the message cycle if there are any messages
    }
});