from flask import Flask, render_template, redirect, request, session, jsonify
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from login_required import login_required
import secrets


app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex()
socketio = SocketIO(app, cors_allowed_origins="*")

chnls = ["General"]
messages = {chnls[0]: []}
session_tmp = {}


@app.route("/")
@login_required
def index():
    return render_template(
        "index.html",
        CHANNELS=chnls,
        user=session["username"],
        current_channel="Inicio",
    )


@app.route("/<channel>", methods=["GET", "POST"])
@login_required
def channel(channel):
    name = session["username"]
    session["current_channel"] = channel
    return render_template(
        "channel.html",
        user=name,
        current_channel=channel,
        msgs=messages[channel],
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    global session_tmp
    if request.method == "POST":
        name = request.form.get("username")
        session["username"] = name
        session["current_channel"] = ""
        session_tmp[name] = ""
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    return redirect("/login")


# AJAX route
@app.route("/get_previous_chnl", methods=["GET"])
@login_required
def get_previous_chnl():
    if session["current_channel"] == "":
        return jsonify({"success": False})
    return jsonify({"success": True, "channel": session["current_channel"]})


@app.context_processor
def charge_channel_list():
    return dict(CHANNELS=chnls)


@socketio.on("create_channel")
def create_channel(new_chnl):
    lwr_chnls = []
    for chnls_item in chnls:
        lwr_chnls.append(chnls_item.lower())

    if new_chnl.lower() in lwr_chnls:
        emit("error", "Ese nombre ya esta en uso", broadcast=False)
    else:
        chnls.append(new_chnl)
        messages[new_chnl] = []
        emit("showChannel", new_chnl, broadcast=True)
    lwr_chnls = []


@socketio.on("enterRoom")
def enter_room():
    user = session["username"]
    chnl = session["current_channel"]

    session_tmp[user] = chnl
    join_room(chnl)
    emit("alertStatus", f"Has entrado al cuarto {chnl}", broadcast=False)
    emit(
        "alertStatus",
        f"{user} ha entrado al cuarto {chnl}",
        broadcast=True,
        include_self=False,
        to=chnl,
    )


@socketio.on("exitRoom")
def exit_room():
    user = session["username"]
    chnl = session_tmp[user]
    if chnl != "":
        leave_room(chnl)
        emit(
            "alertStatus",
            f"{user} ha salido del cuarto",
            broadcast=True,
            include_self=False,
            to=chnl,
        )


@socketio.on("message")
def process_messages(msg, user, date, current_channel):
    messages[current_channel].append(
        {"username": user, "msg": msg, "date": date}
    )

    # Only save 100 messages
    length_channel = len(messages[current_channel])
    if length_channel > 100:
        for i in range(0, length_channel - 100):
            messages[current_channel].pop(0)
    send((msg, user, date), to=current_channel)


@socketio.on("delMsg")
def del_msg(i, cc):
    del messages[cc][i]


if __name__ == "__main__":
    socketio.run(app)
