const socket = io();

// Enter the new room after be redirect
document.addEventListener("DOMContentLoaded", () => {
    if (document.location.pathname != "/") {
        socket.emit("exitRoom");
        socket.emit("enterRoom");
    }
});

// Redirect to previous channel
if (window.location.pathname == "/") {
    /*
     * r is for request, i try to change the name
     * but that broken this functionality
    */
    const r = new XMLHttpRequest();
    r.onload = () => {
        const data = JSON.parse(r.responseText);
        if (data.success) {
            window.location.pathname = data.channel;
        };
    };
    r.open("GET", "/get_previous_chnl");
    r.send();
}

// Create a new channel 
document.querySelector(".createChannel").onclick = () => {
    newChannel = document.querySelector(".newChannel");
    if (newChannel.value) {
        socket.emit("create_channel", newChannel.value);
        newChannel.value = "";
    } else {
        alert("Para crear un chat necesitas insertar un nombre");
    }
};

// Show the new channel
socket.on("showChannel", (channel) => {
    document.querySelector(".channels-list").innerHTML += (`
        <li class="nav-item channel list-group-item">
            <a class="nav-link" href="/${channel}">${channel}</a>
        </li>`
    );
});
