import secrets

from flask import Flask, render_template, redirect, request, session, flash, g
from flask_socketio import SocketIO, emit, join_room, leave_room
from login_required import login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex()
socketio = SocketIO(app)

g.channels = ["General"]

@app.route("/")
@login_required
def index():
    print(f"la lista de channels carga y esto es lo  que tiene {channels}")
    join_room(channels[0])
    return render_template("index.html", username=session["username"], current_channel=g.channels[0])


@app.route("/newChannel", methods=["POST","GET"])
def new_channel():
    lower_channel = []
    name_channel = request.form.get("newChannel")
    for channel in g.channels:
        lower_channel.append(channel.lower())

    if name_channel.lower() in lower_channel:
        flash("This name is alraedy in use")
        lower_channel = []
        return redirect("/")
    else:
        g.channels.append(name_channel)
        lower_channel = []
        join_room(name_channel)
        return render_template("index.html", current_channel=name_channel)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        session["username"] = username
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@socketio.on('message')
def handle_data(msg, username, date):
    print(msg, username, date)
    emit("messageOut", (msg, username, date), broadcast=True)

@socketio.on("entrar")
def entrar(sala):
    # Ingresamos al usuario a la sala
    print(sala)
    join_room(sala)

    # Emitimos un aviso a los usuarios conectados a la sala, exceptuando a la persona que se unio
    emit('mensaje', f'Un usuario ha entrado a la sala {sala}', broadcast=True, include_self=False, to=sala)

    # Mandamos una respuesta al evento emit del cliente
    return f'Te has unido a la sala {sala}'

@socketio.on("salir")
def salir(sala):
    # Ingresamos al usuario a la sala
    leave_room(sala)

    # Emitimos un aviso a los usuarios conectados a la sala, exceptuando a la persona que se unio
    emit('mensaje', f'Un usuario ha salido a la sala {sala}', broadcast=True, include_self=False, to=sala)

    # Mandamos una respuesta al evento emit del cliente
    return f'Te has salido a la sala {sala}'

if __name__ == "__main__":
    socketio.run(app)

