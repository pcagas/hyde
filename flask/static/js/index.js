function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
  }
  
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
  }



const del = document.getElementById('delete');
let isClicked = false;
del.addEventListener('click', () => {

    const ulist = document.getElementById("sim_list");
    const sim_list = ulist.getElementsByTagName('li');
    if(!isClicked){
        for(let i = 0; i < sim_list.length; i++){
            sim_list[i].innerHTML += "<span class='close'>x</span>"
        }
        isClicked = true;
    } else{
        console.log(isClicked);
        for(let i = 0; i < sim_list.length; i++){
            const span = sim_list[i].getElementsByClassName('close')[0];
            span.parentElement.removeChild(span);
        }
        isClicked = false;
    }

    const closebtn = document.getElementsByClassName('close');
    for (let i = 0; i < closebtn.length; i++){
    closebtn[i].addEventListener('click', e => {
        var confBox = confirm("Sure To Delete?");
        if(confBox){
        fetch(`http://${window.location.host}/deleting`, {
            method: 'POST',
            headers: {
                "content-type":"application/json"
            },
            body: JSON.stringify({
                id: e.path[1].id
            }),
            redirect: 'manual'
        })
        ulist.removeChild(e.path[1]);
        }
    })
    } 
})