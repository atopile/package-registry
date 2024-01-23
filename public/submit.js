document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('myForm');
    const submitButton = form.querySelector('button[type="submit"]');
    const loadingIcon = document.getElementById('loading');
    const successIcon = document.getElementById('success');

    form.onsubmit = async function (e) {
        e.preventDefault();

        // Hide submit button and show loading icon
        submitButton.style.display = 'none';
        loadingIcon.style.display = 'block';

        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => (data[key] = value));

        try {
            const response = await fetch('http://127.0.0.1:5001/atopile/us-central1/package', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                // Hide loading icon and show success icon
                loadingIcon.style.display = 'none';
                successIcon.style.display = 'block';
            } else {
                // Handle non-successful responses
                alert('Submission failed!');
            }
        } catch (error) {
            // Handle network errors
            alert('Network error!');
        } finally {
            // Hide loading icon
            loadingIcon.style.display = 'none';
        }
    };
});
