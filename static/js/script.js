// Event name of send in SocketIO is "message"

const socket = io();

document.querySelector("#send").onclick = () => {
    msgIn = document.querySelector("#msg").value;
    socket.send(msgIn);
    msgIn = (" "); 
};

socket.on("messageOut", function (msgOut) {
    document.querySelector("#chat").innerHTML += ("<li>" + msgOut + "</li>");
});
