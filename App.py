from flask import Flask, request
from flask_socketio import SocketIO, emit
from MatchManager import MatchManager

#App.py
app = Flask(__name__)
socketio = SocketIO(app)
matchesmanager = MatchManager()


@socketio.on("connect")
def onConnect():
    emit("message", {"msg": "You are connected"})


@socketio.on("register")
def onRegister(data):
    playerId, name = request.sid, data.get("name")
    player = matchesmanager.addPlayer(playerId, name)
    emit("registered", {"msg": f"You are registred as {player.name}"})


@socketio.on("createlobby")
def onCreateLobby():
    lobbyId = matchesmanager.createLobby()
    emit("newlobbyid", {"msg": f"New lobby created with id:{lobbyId}"})


@socketio.on("enterlobby")
def onJoin(data):
    playerId, lobbyId = request.sid, data.get("lobbyid")
    if matchesmanager.assignPlayerToLobby(lobbyId, playerId):
        emit("enterlobby", {"msg": f"You joined {lobbyId}!"})
    else:
        emit("enterlobby", {"msg": f"Some error occured"})


@socketio.on("quitlobby")
def onQuitLobby(data):
    playerId, lobbyId = request.sid, data("lobbyid")
    matchesmanager.removePlayerFromLobby(playerId, lobbyId)


@socketio.on("disconnect")
def onDisonnect():
    playerId = request.sid
    matchesmanager.removePlayer(playerId)
    emit("message", {"msg": "You are now disconected"})


if __name__ == "__main__":
    socketio.run(app, debug=True)


