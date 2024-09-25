document.addEventListener("DOMContentLoaded", function() {
    const itemsPerPage = 3; // Number of items to show per page
    let currentPage = 1;

    const newsContainer = document.getElementById('news-container');
    const newsItems = Array.from(newsContainer.getElementsByClassName('news-body'));
    const totalItems = newsItems.length;
    const totalPages = Math.ceil(totalItems / itemsPerPage);

    function showPage(page) {
        if (page < 1 || page > totalPages) return; // Boundary checks
        currentPage = page;
        console.log(`Showing pagef${currentPage} of ${totalPages}`); // Debugging log

        console.log(`Showing pagef${currentPage} of ${totalPages}`); // Debugging log

        // Hide all items
        newsItems.forEach(item => item.style.display = 'none');

        // Show items for the current page
        const startIndex = (page - 1) * itemsPerPage;
        const endIndex = Math.min(startIndex + itemsPerPage, totalItems);

        for (let i = startIndex; i < endIndex; i++) {
            newsItems[i].style.display = 'block';
        }

        updatePaginationButtons();
    }

    function updatePaginationButtons() {
        document.getElementById('prev-news-btn').disabled = (currentPage === 1);
        document.getElementById('next-news-btn').disabled = (currentPage === totalPages);
    }

    document.getElementById('prev-news-btn').addEventListener('click', function() {
        if (currentPage > 1) {
            currentPage--;
        console.log(` ${currentPage}`); // Debugging log
            
            showPage(currentPage);
        }
    });

    document.getElementById('next-news-btn').addEventListener('click', function() {
        if (currentPage < totalPages) {
            currentPage++;
        console.log(` ${currentPage}`); // Debugging log

            showPage(currentPage);
        }
    });

    // Initialize the display and pagination
    showPage(currentPage);
});
