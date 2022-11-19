const socket = io();

// That is for each new channel created
function enableEnterChannel() {
    channelsList = document.querySelectorAll(".channel a")
    channelsList.forEach((channel) => {
        channel.onclick = () => {
            socket.emit("exitRoom");
        };
    });
};

document.addEventListener("DOMContentLoaded", () => {
    cc = document.querySelector("#current-channel").value    
    socket.emit("enterRoom", cc);
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
            <a class="nav-link" href="/${channel}">${channel}</a>
        </li>`
    );
    enableEnterChannel();
});

// Enter to channel
enableEnterChannel();

socket.on("alertStatus", (status) => {
    date = new Date();
    dateMsg = `${date.getDate()}/${date.getMonth()} ${date.getHours()}:${date.getMinutes()}min`;
    document.querySelector("#chat").innerHTML += (`
        <li class='list-group-item d-flex justify-content-between align-items-start'>
            <div class="ms-2 me-auto">
                <div class="fw-bold">Flack</div>
                ${status}
            </div>
            <span class="badge bg-primary rounded-pill">${dateMsg}</span>
        </li>
    `);
});

// Change the visibility of the Messages
/*
socket.on("visibilityMsg", function (newCh, oldCh) {
    document.querySelectorAll(`.${oldCh}`).setAttribute("hidden", "");
    document.querySelectorAll(`.${newCh}`).removeAttribute("hidden");
});
*/


