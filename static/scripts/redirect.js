function redirect(time = 5, elementId = 'counter', redirectLocation = '/') {
    const element = document.getElementById(elementId)
    element.innerHTML = time;
    let currentTime = time;

    window.setInterval(() => {
        currentTime--;

        if(currentTime === 0) {
            window.location.href = redirectLocation;
        }

        element.innerHTML = currentTime;
    }, 1000);
}

