import os
import secrets

from flask import Flask, render_template, redirect, request, session
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from login_required import login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex()
socketio = SocketIO(app)


@app.route("/")
@login_required
def index():
    return render_template("index.html", username=session["username"])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        session["username"] = username
        return redirect("/")
    else:
        return render_template("login.html")
   

@socketio.on('message')
def handle_data(msg, username, date):
    print(msg, username, date)
    emit("messageOut", (msg, username, date), broadcast = True)

@socketio.on("crear")
def crear_chat(sala):
    return 

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

