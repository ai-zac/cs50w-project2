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
            <a class="nav-link" href="/channel/#${channel}">${channel}</a>
        </li>`
    );
});

// Enter to channel
document.querySelector(".channel").onclick = () => {
    enterChannel = document.querySelector(".channel").value;
    socket.emit("entrar", enterChannel);
    alert("ya le di click al canal");
};

// Change the visibility of the Messages
socket.on("visibilityMsg", function (newCh, oldCh) {
    document.querySelectorAll(`.${oldCh}`).setAttribute("hidden", "");
    document.querySelectorAll(`.${newCh}`).removeAttribute("hidden");
});

socket.on("mensaje", function (mensaje) {
    document.querySelector("#chat").innerHTML += (`
        ${mensaje}
    `);
});

