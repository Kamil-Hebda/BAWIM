document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('signupButton');
    const form = document.getElementById('signupForm');

    button.addEventListener('click', function() {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {
            username: formData.get('username'),
            password: formData.get('password'),
        };

        fetch('/signup', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if(response.status === 200) {
                window.location.href = '/second_order';
            } else {
                return response.json().then(error => {
                    alert(error.message);
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});