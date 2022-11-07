// Event name of send in SocketIO is "message"
const socket = io();
var username, msgIn, msgOut;

document.querySelector("#send").onclick = () => {
    if (document.querySelector("#name").value) {
        username = document.querySelector("#name").value;
        msgIn = document.querySelector("#msg").value;
        var date = new Date();
        var dateMsg = `${date.getDate()}/${date.getMonth()}-${date.getHours()}:${date.getMinutes()}` 
        socket.send(msgIn, username, dateMsg);
        // clean message
        document.querySelector("#msg").value = "";
    } else {
        alert("Para enviar mensajes necesitas insertar un nombre de usuario")
    }
};

socket.on("messageOut", function (msgOut, username, dateMsg) {
    document.querySelector("#chat").innerHTML += (
        `<li class='list-group-item d-flex justify-content-between align-items-start'>
            <div class="ms-2 me-auto">
                <div class="fw-bold">${username}</div>
                ${msgOut}
            </div>
            <span class="badge bg-primary rounded-pill">${dateMsg}</span>
        </li>`);
});

// respuesta = Es el mensaje de estado, solo se muestra para 
// el propio Usuario
/*
document.querySelector("#boton1").onclick = () => {
    socket.emit("entrar", "CS50x.ni", (respuesta) => {
        document.querySelector("#contenido").append(respuesta)
        document.querySelector("#contenido").innerHTML += "<br>"
        document.querySelector("#msg").className = "CS50x.ni"
        document.querySelector("#salir1").removeAttribute("hidden")
    })
}

document.querySelector('#boton2').onclick = () => {
    socket.emit("entrar", "Web50x.ni", (respuesta) => {
        console.log(respuesta)
        document.querySelector("#contenido").append(respuesta)
        document.querySelector("#contenido").innerHTML += "<br>"
        document.querySelector("#msg").className = "Web50x.ni"
        document.querySelector("#salir2").removeAttribute("hidden")
    })
}

document.querySelector("#salir1").onclick = () => {
    socket.emit("salir", "CS50x.ni", (respuesta) => {
        document.querySelector("#contenido").append(respuesta)
        document.querySelector("#contenido").innerHTML += "<br>"
        document.querySelector("#msg").className = ""
        document.querySelector("#salir1").setAttribute("hidden", true)
    })
}

document.querySelector("#salir2").onclick = () => {
    socket.emit("salir", "Web50x.ni", (respuesta) => {
        document.querySelector("#contenido").append(respuesta)
        document.querySelector("#contenido").innerHTML += "<br>"
        document.querySelector("#msg").className = ""
        document.querySelector("#salir2").setAttribute("hidden", true)
    })
}

// Se indica a los otros usuarios la entrada y salida de 
// los otros usuarios
socket.on("mensaje", (dato) => {
    document.querySelector("#contenido").append(dato)
    document.querySelector("#contenido").innerHTML += "<br>"
})

*/



