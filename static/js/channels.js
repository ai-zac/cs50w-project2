const socket = io();

// Enter the new room after be redirect
document.addEventListener("DOMContentLoaded", () => {
  if (document.location.pathname != "/") {
    socket.emit("exitRoom");
    socket.emit("enterRoom");
  } else if (window.location.pathname == "/") {
    socket.emit("get_previous_channel");
  }
});

socket.on("redirect_channel", (state, channel) => {
  if (state) {
    window.location.pathname = channel;
  }
});

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
  document.querySelector(".channels-list").innerHTML += `
        <li class="nav-item channel list-group-item">
            <a class="nav-link" href="/${channel}">${channel}</a>
        </li>`;
});
