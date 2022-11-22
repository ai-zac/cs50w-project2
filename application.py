import os

from flask import Flask, render_template, redirect, request, session, flash, jsonify
from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms
from login_required import login_required
import secrets


app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex()
socketio = SocketIO(app, cors_allowed_origins='*')
chnls = ["General"]
messages = {chnls[0]: []}
# session out flask's context
session_tmp = {}


@app.route("/")
@login_required
def index():
    return render_template("index.html", CHANNELS=chnls)


@app.route("/<c>", methods=["GET", "POST"])
@login_required
def channel(c):
    u = session["username"]
    session["current_channel"] = c
    return render_template("channel.html", user = u, current_channel = c, msgs = messages[c])


@app.route("/login", methods=["GET", "POST"])
def login():
    global session_tmp
    if request.method == "POST":
        u = request.form.get("username")
        session["username"] = u
        session["current_channel"] = ""
        session_tmp[u] = ""
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/login")

# AJAX route
@app.route("/rmb-chnl", methods=["GET"])
@login_required
def rmb_chnl():
    s = session
    if s["current_channel"] == "":
        return jsonify({"success": False})
    return jsonify({"success": True, "user": s["username"]})


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
    u = session["username"]
    c = session["current_channel"]
    join_room(c)
    session_tmp[u] = c
    emit("alertStatus", f"Has entrado al cuarto {c}", broadcast=False)
    emit("alertStatus", f"{u} ha entrado al cuarto {c}", broadcast=True, include_self=False, to=c)


@socketio.on("exitRoom")
def exit_room():
    u = session["username"]
    c = session_tmp[u]
    if c != "":
        leave_room(c)
        emit("alertStatus", f"{u} ha salido del cuarto" , broadcast=True, include_self=False, to=c)


@socketio.on('message')
def process_messages(m, u, d, cc):
    l = messages[cc]

    # Only save 100 messages
    if len(l) > 100:
        for i in range(0, (len(l) - 100)):
            l.pop(0)
    messages[cc].append({"msg": m, "username": u, "date": d})
    send((m, u, d), to=cc)


if __name__ == "__main__":
    socketio.run(app)
