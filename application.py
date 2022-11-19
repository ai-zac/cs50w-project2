# Debug FLask and Socket
from gevent import monkey
monkey.patch_all()

import os 
import secrets

from flask import Flask, render_template, redirect, request, session, flash
from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms
from login_required import login_required


app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex()
# Debug socoketio: logger and engineio_logger
socketio = SocketIO(app, cors_allowed_origins='*', logger=True, engineio_logger=True)

channels = ["General"] 
channel = ""
messages = {channels[0] : []}
users = {}

@app.route("/")
@login_required
def index():
    return render_template("index.html", CHANNELS=channels)

@app.route("/<current_channel>", methods=["GET", "POST"])
def channel(current_channel):
    session["current_channel"] = users[session["username"]]
    return render_template("channel.html", user = session["username"], c = current_channel, m = messages[current_channel]) 

@app.route("/login", methods=["GET", "POST"])
def login():
    global users
    if request.method == "POST":
        username = request.form.get("username")
        session["username"] = username
        session["current_channel"] = ""
        users[session["username"]] = session["current_channel"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/login")

@app.context_processor
def charge_channel_list():
    return dict(CHANNELS = channels)

@socketio.on("create_channel")
def create_channel(new_channel):
    lower_channels = []
    for channels_item in channels:
        lower_channels.append(channels_item.lower())

    if new_channel.lower() in lower_channels:
        flash("This name is alraedy in use")
    else:
        channels.append(new_channel)
        emit("showChannel", new_channel, broadcast=True) 

    lower_channel = []

@socketio.on("enterRoom")
def enter_room(sala):
    join_room(sala)
    emit("alertStatus", f"Has entrado al cuarto {sala}", broadcast=False)
    emit("alertStatus", f"{session['username']} ha entrado al cuarto {sala}", broadcast=True, include_self=False, to=sala)
    users[session["username"]] = sala

@socketio.on("exitRoom")
def exit_room():
    emit("alertStatus", f"{session['username']} ha salido del cuarto {sala}", broadcast=True, include_self=False, to=users[session["username"]])
    leave_room(users[session["username"]])

@socketio.on('message')
def process_messages(msg, username, date, current_channel):
    m = f""" 
         <li class='list-group-item d-flex justify-content-between align-items-start'>
            <div class="ms-2 me-auto">
                <div class="fw-bold">{username}</div>
                {msg}
            </div>
            <span class="badge bg-primary rounded-pill">{date}</span>
        </li>       
    """
    l = messages[current_channel]
    if len(l) > 100:
        for i in range(0, (len(l) - 100)):
           l.pop(0) 
           
    messages[current_channel].append(m)
    send((msg, username, date), to=current_channel)


if __name__ == "__main__":
    socketio.run(app)

