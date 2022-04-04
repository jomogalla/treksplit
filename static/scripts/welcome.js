document.addEventListener("DOMContentLoaded", async function(event) { 
    const button = document.getElementById('add-group');
    const intro = document.getElementById('intro');
    const spinner = document.getElementById('spinner');
    const recentlyVisitedElement = document.getElementById('recently-visited');
    const copyElement = document.getElementById('copy');
    const exampleElement = document.getElementById('example');

    button.addEventListener('click', async function () {
        intro.style.display = 'none';
        spinner.style.display = 'block';

        try {
            const response = await fetch('/group/0/', {
                method: 'POST',
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
            window.location.href = `/error/${error.message}`;
        } 
    });

    function populateRecentlyVisited() {
        const list = document.createElement('ul');
        let hasVisits = false;

        for(const hash in recentlyVisited.visited) {
            hasVisits = true;
            const name = recentlyVisited.visited[hash];

            const listItem = document.createElement('li');

            const newLink = document.createElement('a');
            newLink.setAttribute('href', hash);
            newLink.innerText = `view ${name} `;
            newLink.classList.add('text_button');
            const arrow = document.createElement('i');
            arrow.classList.add('fa');
            arrow.classList.add('fa-arrow-right');
            newLink.appendChild(arrow);

            listItem.appendChild(newLink)

            list.appendChild(listItem);
        }

        recentlyVisitedElement.appendChild(list)
        if(hasVisits) {
            recentlyVisitedElement.style.display = 'block';
            copyElement.style.display = 'none';
            exampleElement.style.display = 'none';
        }
    }

    populateRecentlyVisited();
});