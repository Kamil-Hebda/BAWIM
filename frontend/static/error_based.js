document.addEventListener('DOMContentLoaded', function (event) {
    const button = document.getElementById('signupButton');
    const form = document.getElementById('signupForm');

    button.addEventListener('click', function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {
            username: formData.get('username'),
            password: formData.get('password')
        };

        fetch('/signup_error', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => {
                return response.json();
            })
            .then(data => { 
                document.getElementById('modal-message').innerText = data.message;
                document.getElementById('modal-sql-query').innerText = data.feedback;
                const modal = new bootstrap.Modal(document.getElementById('resultModal'));
                modal.show();
            })
            .catch(error => {
                alert('Error: ' + error);
                console.error('Error:', error);
            });
    });

    loginButton.addEventListener('click', function (event) {
        event.preventDefault();

        console.log('login button clicked');

        const formData = new FormData(form);
        const data = {
            username: formData.get('username'),
            password: formData.get('password'),
        };

        fetch('/error_login', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => {
                if (response.status === 200) {
                    return response.json();
                } else {
                    return response.json().then(error => {
                        throw new Error(error.message);
                    });
                }
            })
            .then(data => {
                document.getElementById('modal-message').innerText = data.message;
                document.getElementById('modal-sql-query').innerText = data.feedback;
                const modal = new bootstrap.Modal(document.getElementById('resultModal'));
                modal.show();
            })
            .catch(error => {
                alert("Brak takiego użytkownika");
            });
    });
});

function redirectToHome() {
    window.location.href = '/';
}
