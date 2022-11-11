import secrets

from flask import Flask, render_template, redirect, request, session, flash
from flask_socketio import SocketIO, emit, join_room, leave_room
from login_required import login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex()
socketio = SocketIO(app, cors_allowed_origins='*')

channels = ["General"] 
messages = {channels[0] : []}

@app.route("/")
@login_required
def index():
    print(f"El canal actual es {session['current_channel']}")
    return render_template("index.html", username=session["username"]) 

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        session["username"] = username
        session["current_channel"] = "General"
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@socketio.on('message')
def message(msg, username, date):
    print(msg, username, date)
    join_room(session["current_channel"])
    emit('messageOut', (msg, username, date, session["current_channel"]), broadcast=True, to=session["current_channel"])

@socketio.on("create_channel")
def new_channel(channel):
    print("Se esta ejecutanto create_channel")
    print(f"channel is {channel}")
    lower_channel = []
    for channelsItem in channels:
        lower_channel.append(channelsItem.lower())

    if channel.lower() in lower_channel:
        print("No se creo el chat")
        print(f"la lista de canales actuales es: {lower_channel}")
        flash("This name is alraedy in use")
    else:
        print("Si se creo el chat")
        channels.append(channel)
        leave_room(session["current_channel"])
        print(f"la session de {session['username']} esta en {session['current_channel']}") 
        emit("newChannel", channel, broadcast=True) 

    lower_channel = []

@socketio.on("entrar")
def entrar(sala):
    # Ingresamos al usuario a la sala
    leave_room(session["current_channel"])
    join_room(sala)

    # Emitimos un aviso a los usuarios conectados a la sala, exceptuando a la persona que se unio
    emit('mensaje', f'Un usuario ha entrado a la sala {sala}', broadcast=True, include_self=False, to=sala)
    
    emit('visibilityMsg', (sala, session["current_channel"])) 
    # Mandamos una respuesta al evento emit del cliente
    session["current_channel"] = sala 
    return f'Te has unido a la sala {sala}'


if __name__ == "__main__":
    socketio.run(app)

