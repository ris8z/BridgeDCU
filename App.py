from flask import Flask, request
from flask_socketio import SocketIO, emit
from MatchManager import MatchManager
from game import Game

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
    response = {
        "msg": f"You are registred as {player.name}",
        "playerName": player.name,
    }
    print(f"{player} has connected")
    emit("registered", response)


@socketio.on("createlobby")
def onCreateLobby():
    lobbyId = matchesmanager.createLobby()
    owner = matchesmanager.players.get(request.sid)

    response = {
        "msg": f"New lobby created with id:{lobbyId}",
        "lobbyId": lobbyId,
    }

    print(f"{matchesmanager.lobbies[lobbyId]} has been created by {owner}")
    emit("newlobbyid", response)



def updateTurnBid(lobbyId:str):
    lobby = matchesmanager.lobbies[lobbyId]
    idx = lobby.game.currentRound.bidPhase.current_turn
    emit("youTurnBid", {"msg": "it is your turn"}, to=lobby.players[idx].id)

@socketio.on("enterlobby")
def onJoin(data):
    playerId, lobbyId = request.sid, data.get("lobbyId")
    if matchesmanager.assignPlayerToLobby(lobbyId, playerId):
        player, lobby = matchesmanager.players[playerId], matchesmanager.lobbies[lobbyId]
        print(f"{player} joined {lobby}")
        emit("enterlobby", {
            "msg": f" {str(player)} joined {str(lobby)}",
            "lobbyId":lobbyId,
            "players": str(lobby.players)
             }, to=lobbyId)

        try:
            matchesmanager.tryToStartGame(lobbyId)
            for p in lobby.players:
                print("game started giving and to", str(p))
                emit("gameStart", {"msg": "The game has started", "hand": str(p.hand)}, to=p.id)
            updateTurnBid(lobbyId)
        except ValueError as e:
            emit("gameStart", {"msg": str(e)}, to=lobbyId)

    else:
        emit("enterlobby", {"msg": f"Test Some error occured while joining the lobby", "lobbyId":""})


@socketio.on("quitlobby")
def onQuitLobby(data):
    playerId, lobbyId = request.sid, data("lobbyid")
    matchesmanager.removePlayerFromLobby(playerId, lobbyId)


@socketio.on("disconnect")
def onDisonnect():
    playerId = request.sid
    print(f"{matchesmanager.players[playerId]} has disconected")
    matchesmanager.removePlayer(playerId)
    emit("message", {"msg": "You are now disconected"})


@socketio.on("makebid")
def onMakeBid(data):
    playerId = request.sid
    lobbyId = data["lobbyId"]
    bid = data["bid"]

    try:
        isBiddingOver = matchesmanager.handleBid(playerId, lobbyId, bid)
        print(isBiddingOver)
        if isBiddingOver:
            emit("bidding_complete", {
                'contract': matchesmanager.lobbies[lobbyId].game.getContract().to_dict(),
                'msg': 'bidding phase is over'
            }, to=lobbyId)
        else:
            updateTurnBid(lobbyId)
    except ValueError as e:
        emit("error", {'msg': str(e)}, to=playerId)


if __name__ == "__main__":
    socketio.run(app, debug=True)
