const socket = io();

// That is for each new channel created
function enableEnterChannel() {
    channelsList = document.querySelectorAll(".channel a")
    channelsList.forEach((channel) => {
        channel.onclick = () => {
            socket.emit("exitRoom");
            socket.emit("enterRoom", channel.text);
            document.querySelector("#current-channel").setAttribute("value", channel.text);
        };
    });
};

window.addEventListener("DOMContentLoaded", () => {
    
});


// Create a new channel 
document.querySelector(".createChannel").onclick = () => {
    if (document.querySelector(".newChannel").value) {
        newChannel = document.querySelector(".newChannel");
        socket.emit("create_channel", newChannel.value);
        newChannel.value = "";
    } else {
        alert("Para crear un chat necesitas insertar un nombre");
    }
};

// Show the new channel
socket.on("showChannel", (channel) => {
    alert("SE EJECUTO showChannel");
    document.querySelector(".channels-list").innerHTML += (
       `<li class="nav-item channel">
            <a class="nav-link" href="#">${channel}</a>
        </li>`
    );
    enableEnterChannel();
});

// Enter to channel
enableEnterChannel();

socket.on("alertStatus", (status) => {
    document.querySelector("#chat").innerHTML += (`
        <li class='list-group-item d-flex justify-content-between align-items-start'>
            <div class="ms-2 me-auto">
                ${status}
            </div>
    `);
});

// Change the visibility of the Messages
/*
socket.on("visibilityMsg", function (newCh, oldCh) {
    document.querySelectorAll(`.${oldCh}`).setAttribute("hidden", "");
    document.querySelectorAll(`.${newCh}`).removeAttribute("hidden");
});
*/


