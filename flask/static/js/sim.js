window.addEventListener('load', () => {
    const add_form = document.getElementById("add_form");
    add_form.addEventListener('submit', e => {
        e.preventDefault();
        const path = new URL(window.location).pathname.split('/'); // ["", "sim", "uuid"]
        const id = path[path.length - 1];
        const name = e.target[0].value;
        const inpFile = editor.getValue();
        fetch(`http://${window.location.host}/adding`, { //fetch API, sending info to this url with optional parameters
            method: 'POST',
            headers: {
                "content-type":"application/json"
            },
            body: JSON.stringify({
                id,
                name,
                inpFile
            }),
            redirect: 'manual'
        })
        .then(result => result.json())
        .then(data =>window.location.assign(data.path))
    });
});