document.addEventListener('DOMContentLoaded', function() {
    const testimonialsData = window.testimonials;
    const testimonialsPerPage = 5; // Number of testimonials to show per page
    let currentPage = 0;

    function renderTestimonials() {
        const container = document.querySelector('.testimonial-boxes');
        container.classList.add('fade-out');

        // Add delay to allow fade-out effect
        setTimeout(() => {
            container.innerHTML = ''; // Clear the container
            const start = currentPage * testimonialsPerPage;
            const end = Math.min(start + testimonialsPerPage, testimonialsData.length);

            for (let i = start; i < end; i++) {
                const testimonial = testimonialsData[i];
                const testimonialBox = document.createElement('div');
                testimonialBox.className = 'testimonial-box animate-in';
                testimonialBox.innerHTML = `
                    <p id="quote">${testimonial.quote}</p>
                    <p id="author">${testimonial.author}</p>
                    <p id="relation">${testimonial.relation}</p>
                `;
                container.appendChild(testimonialBox);
            }

            // Add or remove the empty-state class based on the number of testimonials
            if (testimonialsData.length <= testimonialsPerPage) {
                container.classList.add('empty-state');
            } else {
                container.classList.remove('empty-state');
            }

            // Allow fade-in effect
            container.classList.remove('fade-out');
            container.classList.add('fade-in');
            setTimeout(() => container.classList.remove('fade-in'), 500); // Remove fade-in class after animation
        }, 500); // Duration of fade-out effect
    }

    function nextTestimonials() {
        if (currentPage < Math.ceil(testimonialsData.length / testimonialsPerPage) - 1) {
            currentPage++;
            renderTestimonials();
        }
    }

    function prevTestimonials() {
        if (currentPage > 0) {
            currentPage--;
            renderTestimonials();
        }
    }

    // Initial render
    renderTestimonials();

    // Attach event listeners to buttons
    document.getElementById('prev-btn').addEventListener('click', prevTestimonials);
    document.getElementById('next-btn').addEventListener('click', nextTestimonials);
});
