// static/js/form_navigation.js

document.addEventListener('DOMContentLoaded', function() {
    loadForm('school');  // Start with the school form
});

// Function to retrieve the CSRF token from the cookie
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Function to load a form via AJAX
function loadForm(formName) {
    const url = `/school/load-form/${formName}/`;  // Django view to load form HTML

    fetch(url)
        .then(response => response.text())
        .then(html => {
            document.getElementById('form-container').innerHTML = html;
            // Optionally initialize any JavaScript for the form here (like event listeners)
        })
        .catch(error => console.error('Error loading form:', error));
}

// Function to navigate between forms
function navigateForm(direction) {
    const formSequence = ['school', 'navigation', 'banner', 'about', 'news', 'testimonial', 'footer'];  // Maintain the sequence of the forms
    let currentFormIndex = formSequence.indexOf(document.querySelector('form').id.replace('-form', ''));

    if (direction === 'next' && currentFormIndex < formSequence.length - 1) {
        loadForm(formSequence[currentFormIndex + 1]);
    } else if (direction === 'prev' && currentFormIndex > 0) {
        loadForm(formSequence[currentFormIndex - 1]);
    }
}

// Function to submit form data via AJAX
function submitForm(formName) {
    const form = document.getElementById(`${formName}-form`);
    const formData = new FormData(form);
    const url = `/school/submit-form/${formName}/`;

    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCsrfToken()  // Include the CSRF token
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updatePreview();  // Update the preview after successful submission
                navigateForm('next');  // Go to the next form
            } else {
                // Handle form submission errors
                alert('There was an error submitting the form. Please check the data and try again.');
            }
        })
        .catch(error => console.error('Error submitting form:', error));
}

// Function to update the live preview iframe
function updatePreview() {
    // Here you would either refresh the iframe src to a Django view that renders the preview
    // Or you would use AJAX to fetch the preview HTML and set the innerHTML of the iframe's document
    // For this example, let's assume we're setting the innerHTML directly

    const previewFrame = document.getElementById('preview-frame');
    const formData = new FormData(document.querySelector('form'));

    fetch('/school/update-preview/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCsrfToken()  // Include the CSRF token
        }
    })
        .then(response => response.text())
        .then(html => {
            previewFrame.contentWindow.document.open();
            previewFrame.contentWindow.document.write(html);
            previewFrame.contentWindow.document.close();
        })
        .catch(error => console.error('Error updating preview:', error));
}
