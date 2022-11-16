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
    global channels
    return render_template("index.html", CHANNELS=channels)

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
def context_processor():
    return dict(username=session, CHANNELS=channels)

@socketio.on("create_channel")
def create_channel(new_channel):
    lower_channels = []
    for channels_item in channels:
        lower_channels.append(channels_item.lower())

    if new_channel.lower() in lower_channels:
        flash("This name is alraedy in use")
    else:
        emit("showChannel", new_channel, broadcast=True) 

    lower_channel = []

@socketio.on("enterRoom")
def enter_room(sala):
    join_room(sala)
    send((f"Has entrado al cuarto {sala}", "Flack", "Now"), to=sala)
    rooms()
    users[session["username"]] = sala

@socketio.on("exitRoom")
def exit_room():
    leave_room(users[session["username"]])

@socketio.on('message')
def process_messages(msg, username, date, current_channel):
    send((msg, username, date), to=current_channel)


if __name__ == "__main__":
    socketio.run(app)

