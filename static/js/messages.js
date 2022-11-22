// Send and process the messages 
document.querySelector("#send").onclick = () => {
    date = new Date();
    dateMsg = `${date.getDate()}/${date.getMonth()} ${date.getHours()}:${date.getMinutes()}min`;
    username = document.querySelector("#username").value;
    msgIn = document.querySelector(".msg");
    currentChannel = document.querySelector("#current-channel").value;
    socket.send(msgIn.value, username, dateMsg, currentChannel);
    msgIn.value = "";
};


// Show the messages
socket.on("message", (msgOut, username, dateMsg) => {
    document.querySelector("#chat").innerHTML += (
        `<li class='list-group-item d-flex justify-content-between align-items-start '>
            <div class="ms-2 me-auto text-break">
                <div class="fw-bold">${username}</div>
                ${msgOut}
            </div>
            <span class="badge bg-primary rounded-pill">${dateMsg}</span>
        </li>`);
});

// Alert where are you, "do you know the way"
socket.on("alertStatus", (status) => {
    document.querySelector(".toast-container").innerHTML += (`
        <div class="toast show" role="alert" aria-live="assertive" aria-atomic="true" display="block">
            <div class="toast-header">
                <img src="#" class="rounded me-2" alt="...">
                <strong class="me-auto">Flack</strong>
                <small class="text-muted">just now</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${status}
            </div>
        </div>   
    `);
});

socket.on("error", (msg) => {
    alert(`${msg}`)
});
