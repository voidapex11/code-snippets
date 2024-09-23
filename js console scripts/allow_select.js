// mostly gpt's work

const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))

while (true) {
    sleep
    // Re-enable text selection by removing any CSS that prevents it
    document.querySelectorAll('*').forEach(element => {
        element.style.userSelect = 'text';
        element.style.webkitUserSelect = 'text';
        element.style.mozUserSelect = 'text';
        element.style.msUserSelect = 'text';
    });

    // Remove any event listeners that prevent text selection
    document.addEventListener('selectstart', event => event.stopPropagation(), true);
    document.addEventListener('mousedown', event => event.stopPropagation(), true);
    document.addEventListener('mousemove', event => event.stopPropagation(), true);
    document.addEventListener('mouseup', event => event.stopPropagation(), true);
    await sleep(1000)
}
 
