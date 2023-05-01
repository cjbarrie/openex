document.addEventListener('DOMContentLoaded', function () {
    const mainForm = document.querySelector('form#main-form');

    if (mainForm) {
        mainForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const nameInput = document.getElementById('name');
            const emailInput = document.getElementById('email');

            if (nameInput.value === '' || emailInput.value === '') {
                alert('Please fill in all the fields');
                return;
            }

            // Perform form submission (e.g., send data to the server)
            mainForm.submit();
        });
    }
});
