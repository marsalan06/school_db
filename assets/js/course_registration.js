document.addEventListener('DOMContentLoaded', function () {
    // Set the date we're counting down to
    var countDownDate = new Date("Aug 31, 2024 23:59:59").getTime();
    
    // Update the count down every 1 second
    var x = setInterval(function() {
      
        // Get the current date and time
        var now = new Date().getTime();
        
        // Calculate the time remaining
        var distance = countDownDate - now;
        
        // Time calculations for days, hours, minutes and seconds
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
        // Display the result in the elements
        document.querySelector('.coming-soon .days .value').innerText = days < 10 ? '0' + days : days;
        document.querySelector('.coming-soon .hours .value').innerText = hours < 10 ? '0' + hours : hours;
        document.querySelector('.coming-soon .minutes .value').innerText = minutes < 10 ? '0' + minutes : minutes;
        document.querySelector('.coming-soon .seconds .value').innerText = seconds < 10 ? '0' + seconds : seconds;
        
        // If the countdown is over, display a message
        if (distance < 0) {
            clearInterval(x);
            document.querySelector('.coming-soon h4').innerText = "The offer has ended!";
            document.querySelector('.coming-soon .counter').style.display = 'none';
        }
    }, 1000);
});
