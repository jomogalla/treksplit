document.addEventListener("DOMContentLoaded", async function(event) { 
    const button = document.getElementById('add_group');
    const intro = document.getElementById('intro');
    const spinner = document.getElementById('spinner');

    button.addEventListener('click', async function () {
        intro.style.display = 'none';
        spinner.style.display = 'block';

        try {
            const response = await fetch('/group/0/', {
                method: 'POST',
                body: '',
                credentials: 'same-origin',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            })

            if (response.status !== 200) {
                throw new Error(response.status);
            }
    
            const hash = await response.text();

            window.location.href = `/${hash}`;
        } catch(error) {

        } 
    });
});