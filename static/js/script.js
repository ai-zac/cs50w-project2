// Event name of send in SocketIO is "message"

const socket = io();
var username, msgIn, msgOut;
let i = 0;

document.querySelector("#send").onclick = () => {
    if (document.querySelector("#name").value) {
        username = document.querySelector("#name").value;
        msgIn = document.querySelector("#msg").value;

        socket.send(msgIn, username);
        localStorage.setItem("message" + i, "{'username': " + username + ", 'msg': " + msgIn + "}") 
        i++;
        // clean message
        document.querySelector("#msg").value = "";
    } else {
        alert("Para enviar mensajes necesitas insertar un nombre de usuario")
    }
};

socket.on("messageOut", function (msgOut, username) {
    document.querySelector("#chat").innerHTML += ("<li>" + username + ": " + msgOut + "</li>");
});
