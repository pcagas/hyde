window.addEventListener('load', () => {
//    const plad = document.getElementById("plot_form")
//    plad.addEventListener('submit', () => {
//	e.preventDefault();
//	const path = new URL(window.location).pathname.split('/');//["", "sim", "uuid", "plot"]
//	const id = path[path.length - 2];
//	fetch(`http://${window.location.host}/plot`, {
//	    method: 'POST',
//	    headers: {
//		"content-type":"application/json"
//	    },
//	    body: JSON.stringify({
//		id,
//		path
//	    }),
//	    redirect: 'manual'
//	})
//	    .then(result => result.json())
//  });

    const plot = document.getElementById("plot")
    run.addEventListener('click', () => {
	const path = new URL(window.location).pathname.split('/');
	const id = path[path.length - 1];
	fetch(`http://${window.location.host}/plot`, {
	    method: 'POST',
	    headers: {
		"content-type":"application/json"
	    },
	    body: JSON.stringify({
		id
	    }),
	    redirect: 'manual'
	})
    });
});
