from flask import Flask, request
from flask_socketio import SocketIO, emit
from MatchManager import MatchManager
from game import Game
from Card import Card, Suits, Values

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
    emit("registered", {
        "msg": f"You are registred as {player.name}",
        "playerName": player.name,
    })


@socketio.on("createlobby")
def onCreateLobby():
    lobbyId = matchesmanager.createLobby()
    emit("newlobbyid", {
        "msg": f"New lobby created with id:{lobbyId}",
        "lobbyId": lobbyId,
    })


def addPlayer(lobbyId:str, playerId:str):
    matchesmanager.assignPlayerToLobby(lobbyId, playerId)
    player, lobby = matchesmanager.players[playerId], matchesmanager.lobbies[lobbyId]
    emit("enterlobby", {
         "msg": f" {str(player)} joined {str(lobby)}",
         "lobbyId":lobbyId,
         "players": str(lobby.players)
    }, to=lobbyId)


def dealCards(lobbyId:str):
    lobby = matchesmanager.lobbies[lobbyId]
    for p in lobby.players:
        print("game started giving and to", str(p))
        emit("gameStart", {"msg": "The game has started", "hand": str(p.hand)}, to=p.id)


def updateTurnBid(lobbyId:str):
    lobby = matchesmanager.lobbies[lobbyId]
    idx = lobby.game.currentRound.bidPhase.current_turn
    emit("youTurnBid", {"msg": "it is your turn to bid",
                        "hand":",".join([str(c) for c in lobby.players[idx].hand]),
                        "format": "1,H or 2,C or pass"
    }, to=lobby.players[idx].id)


def tryStartGame(lobbyId:str):
    matchesmanager.tryToStartGame(lobbyId)
    dealCards(lobbyId)
    updateTurnBid(lobbyId)


@socketio.on("enterlobby")
def onJoin(data):
    playerId, lobbyId = request.sid, data.get("lobbyId")
    try:
        addPlayer(lobbyId, playerId)
        tryStartGame(lobbyId)
    except ValueError as e:
        emit("error", {"msg": str(e)})


@socketio.on("makebid")
def onMakeBid(data):
    playerId = request.sid
    lobbyId = data["lobbyId"]
    bid = data["bid"]

    try:
        lobby = matchesmanager.lobbies.get(lobbyId)
        if not lobby:
            raise ValueError("lobby not exist")

        isBiddingOver = matchesmanager.handleBid(playerId, lobbyId, bid)
        print(isBiddingOver)

        #emit to the lobby who did the bid and how much it is
        emit("bidMade", {"msg": "a bid was made", "player": lobby.getIdx(playerId), "bid":bid}, to=lobbyId)

        if isBiddingOver:
            emit("bidding_complete", {
                'contract': matchesmanager.lobbies[lobbyId].game.getContract().to_dict(),
                'msg': 'bidding phase is over'
            }, to=lobbyId)
            updateTurnPlay(lobbyId) # start the first round
        else:
            updateTurnBid(lobbyId)
    except ValueError as e:
        emit("error", {'msg': str(e)}, to=playerId)



def updateTurnPlay(lobbyId:str):
    lobby = matchesmanager.lobbies[lobbyId]
    idx = lobby.game.currentRound.trickPhase.current_turn
    if lobby.game.currentRound.trickPhase.flag:
        emit("youturnplayfordummy", {"msg": "it is your turn to play for your dummy",
                                     "hand":",".join([str(c) for c in lobby.players[(idx + 2) % 4].hand])
        }, to=lobby.players[idx].id)
    else:
        emit("youTurnPlay", {"msg": "it is your turn to play",
                             "hand":",".join([str(c) for c in lobby.players[idx].hand])
        }, to=lobby.players[idx].id)

@socketio.on("makeplay")
def onMakePlay(data):
    print(data)
    playerId = request.sid
    lobbyId = data["lobbyid"]
    cardValue = data["cardvalue"]
    cardSuite = data["cardsuite"]

    try:
        cardObj = Card(Values(cardValue), Suits(cardSuite))
        lobbyObj = matchesmanager.lobbies.get(lobbyId)
        if not lobbyObj:
            raise ValueError("Lobby does not exist")

        GameObj = lobbyObj.game
        if not GameObj:
            raise ValueError("Game not yet started in this lobby")

        isThisTrickCompleted = GameObj.makePlay(playerId, cardObj)

        # emit to the lobby who played the card and which card
        emit("cardPlayed", {"msg": "a card was played", "player": lobbyObj.getIdx(playerId), "cardvalue": cardValue, "cardsuite": cardSuite}, to=lobbyId)

        if isThisTrickCompleted:
            emit("newtrick_completed", {
                'trick': GameObj.getLastTrick().toDict(),
                'winnerIdx': GameObj.getLastTrick().winner(),
                'msg': 'a new trick has been completed'
            }, to=lobbyId)

            if GameObj.currentRound and GameObj.currentRound.isRoundOver():
                #no more tricks to play for this round
                GameObj.endCurrentRound()

                if not GameObj.isGameOver():
                    GameObj.startNewRound()
                    dealCards(lobbyId)
                    updateTurnBid(lobbyId)
                else:
                    print("The game is ended")
                    #the game is endend return a list of round
                    emit("gameOver", {
                        "msg": "the game is over",
                        "points": GameObj.points
                    }, to=lobbyId)
            else:
                #there is some tricks to play for this round
                updateTurnPlay(lobbyId)
        else:
            updateTurnPlay(lobbyId)
    except ValueError as e:
        print(e)
        emit("error", {'msg': str(e)}, to=playerId)





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


if __name__ == "__main__":
    socketio.run(app, debug=True)
