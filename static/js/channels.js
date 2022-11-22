const socket = io();

document.addEventListener("DOMContentLoaded", () => {
    if (document.location.pathname != "/") {
        socket.emit("exitRoom");
        socket.emit("enterRoom");
    } 
});

// Redirect to current channel
if (window.location.pathname == "/") {
    const r = new XMLHttpRequest();
    r.onload = () => {
        const data = JSON.parse(r.responseText);
        if (data.success) {
            p = localStorage.getItem(data.user);
            window.location.pathname = p;
        };
    };
    r.open("GET", "/rmb-chnl");
    r.send();
} else {
    // save the current session
    u = document.querySelector("#username").value;
    cc = document.querySelector("#current-channel").value;
    localStorage.setItem(u, cc);
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
    document.querySelector(".channels-list").innerHTML += (
        `<li class="nav-item channel">
            <a class="nav-link" href="/${channel}">${channel}</a>
        </li>`
    );
});

// Alert where are you, "do you know the way"
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

socket.on("error", (msg) => {
    alert(`${msg}`)
});
