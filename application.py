import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")

@socketio.on('message')
def handle_data(msg, username):
    print(msg, username)
    emit("messageOut", (msg, username), broadcast = True)


if __name__ == "__main__":
    socketio.run(app)

