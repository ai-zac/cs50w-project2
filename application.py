from flask import Flask, flash, render_template, redirect, request, session, jsonify
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from tools import channel_find, login_required
import secrets


app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex()
socketio = SocketIO(app, cors_allowed_origins="*")

# FLASK's variables 
CHANNELS = ["General"]
db_messages = {CHANNELS[0]: []}

# SocketIO's variable 
previous_channel = {}


@app.route("/")
@login_required
def index():
    return render_template(
        "index.html",
        CHANNELS=CHANNELS,
        USER=session["username"],
        STR_CURRENT_CHANNEL="Inicio",
    )


@app.route("/<channel>")
@login_required
def redirect_channel(channel):
    if not channel_find(channel, db_messages):
        return redirect("/")

    session["current_channel"] = channel

    return render_template(
        "channel.html",
        USER=session["username"],
        STR_CURRENT_CHANNEL=session["current_channel"],
        LIST_MESSAGES=db_messages[channel],
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form.get("username")
        session["current_channel"] = None
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    return redirect("/login")


@app.context_processor
def charge_channel_list():
    return dict(CHANNELS=CHANNELS)


@socketio.on("create_channel")
def create_channel(new_chnl):
    lwr_channel = []
    for channel_item in CHANNELS:
        lwr_channel.append(channel_item.lower())

    if new_chnl.lower() in lwr_channel:
        emit("error", "That name is already used", broadcast=False)
    else:
        CHANNELS.append(new_chnl)
        db_messages[new_chnl] = []
        emit("showChannel", new_chnl, broadcast=True)
    lwr_channel = []


@socketio.on("exitRoom")
def exit_room():
    user = session["username"]
    channel = previous_channel[user]
    if channel != None:
        leave_room(channel)
        emit(
            "alertStatus",
            f"{user} leaves {channel}",
            broadcast=True,
            include_self=False,
            to=channel,
        )


@socketio.on("enterRoom")
def enter_room():
    user = session["username"]
    channel = session["current_channel"]
    previous_channel[user] = channel

    join_room(channel)
    emit("alertStatus", f"You have joined {channel}", broadcast=False)
    emit(
        "alertStatus",
        f"{user} has joined {channel}",
        broadcast=True,
        include_self=False,
        to=channel,
    )


@socketio.on("message")
def process_messages(msg, user, date, current_channel):
    db_messages[current_channel].append(
        {"username": user, "msg": msg, "date": date}
    )

    # Only save 100 messages
    length_channel = len(db_messages[current_channel])
    if length_channel > 100:
        for i in range(0, length_channel - 100):
            db_messages[current_channel].pop(0)
    send((msg, user, date), to=current_channel)


@socketio.on("get_previous_channel")
def get_previous_channel():
    if session["current_channel"] == None:
        emit("redirect_channel", (False, "/"), broadcast=False)
    else:
        emit("redirect_channel", (True, session["current_channel"]), broadcast=False) 



@socketio.on("delMsg")
def del_msg(i, cc):
    del db_messages[cc][i]


if __name__ == "__main__":
    socketio.run(app)
