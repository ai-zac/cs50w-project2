// Send and process the messages 
document.querySelector("#send").onclick = () => {
    date = new Date();
    d = `${date.getDate()}/${date.getMonth()} ${date.getHours()}:${date.getMinutes()}min`;
    u = document.querySelector("#username").value;
    m = document.querySelector(".msg");
    cc = document.querySelector("#current-channel").value;
    socket.send(m, u, d, cc);
    document.querySelector(".msg").value = "";
};


// Show the messages
socket.on("message", (msgOut, username, dateMsg) => {
    alert("SE EJECUTO EL showMessage");
    document.querySelector("#chat").innerHTML += (
        `<li class='list-group-item d-flex justify-content-between align-items-start'>
            <div class="ms-2 me-auto">
                <div class="fw-bold">${username}</div>
                ${msgOut}
            </div>
            <span class="badge bg-primary rounded-pill">${dateMsg}</span>
        </li>`);
});


