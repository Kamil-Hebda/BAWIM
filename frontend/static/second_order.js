document.addEventListener('DOMContentLoaded', function(event) {
    const button = document.getElementById('signupButton');
    const form = document.getElementById('signupForm');

    button.addEventListener('click', function() {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {
            username: formData.get('username'),
            password: formData.get('password')
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
                window.location.href = '/second_order_sqli';
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

    loginButton.addEventListener('click', function (event) {
        event.preventDefault();

        console.log('login button clicked');

        const formData = new FormData(form);
        const data = {
            username: formData.get('username'),
            password: formData.get('password'),
        };

        fetch('/login', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    return response.json().then(error => {
                        throw new Error(error.message);
                    });
                }
            })
            .then(data => {
                console.log(data.message);
                alert(data.message);
            })
            .catch(error => {
                console.error('Error:', error);
                alert(error.message);
            });
    });
});
