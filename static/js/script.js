// Event name of send in SocketIO is "message"
const socket = io();

// Send the messages 
document.querySelector("#send").onclick = () => {
    var date = new Date();
    var dateMsg = `${date.getDate()}/${date.getMonth()} ${date.getHours()}:${date.getMinutes()}min`;
    username = document.querySelector("#username").value;
    msgIn = document.querySelector(".msg").value;
    socket.send(msgIn, username, dateMsg);
    document.querySelector(".msg").value = "";
};


// View the messages
socket.on("messageOut", function (msgOut, username, dateMsg, currentChannel) {
    alert("SE EJECUTO EL messageOut");
    document.querySelector("#chat").innerHTML += (
        `<li class='${currentChannel} list-group-item d-flex justify-content-between align-items-start'>
            <div class="ms-2 me-auto">
                <div class="fw-bold">${username}</div>
                ${msgOut}
            </div>
            <span class="badge bg-primary rounded-pill">${dateMsg}</span>
        </li>`);
});

// Create new channel 
document.querySelector(".createChannel").onclick = () => {
    alert("SE EJECUTO createChannel")
    if (document.querySelector(".newChannel").value) {
        newChannel = document.querySelector(".newChannel").value;
        socket.emit("create_channel", newChannel);
        document.querySelector(".newChannel").value = "";
    } else {
        alert("Para crear un chat necesitas insertar un nombre");
    }
};

// Show the new channel
socket.on("newChannel", function (channel) {
    alert("SE EJECUTO newChannel")
    document.querySelector(".channels-list").innerHTML += (
       `<li class="nav-item channel">
            <a class="nav-link" href="#">${channel}</a>
        </li>`
    );
});

// Enter to channel
document.querySelector(".channel").onclick = () => {
    enterChannel = document.querySelector(".channel").value;
    socket.emit("entrar", enterChannel);
};

socket.on("visibilityMsg", function (newCh, oldCh) {
    document.querySelectorAll(`.${oldCh}`).setAttribute("hidden", "");
    document.querySelectorAll(`.${newCh}`).removeAttribute("hidden");
});

