from lobby import Lobby
import random
from game import Game
from player import Player
from lobby import Lobby
from typing import Dict


class MatchManager(object):
    def __init__(self):
        self.players: Dict[str, Player] = {}
        self.lobbies: Dict[str, Lobby] = {}

    def addPlayer(self, playerId: str, name: str) -> Player:
        player = Player(playerId, name)
        self.players[playerId] = player
        return player

    def removePlayer(self, playerId) -> bool:
        player = self.players.get(playerId, None)
        if player and player.lobbyId:
            self.removePlayerFromLobby(player.lobbyId, playerId)
            del self.players[playerId]
            return True
        return False

    def removePlayerFromLobby(self, lobbyId: str, playerId: str) -> bool:
        player = self.players.get(playerId)
        lobby = self.lobbies.get(lobbyId)
        if lobby and player in lobby.players:
            lobby.removePlayer(player)
            player.quitLobby()
            if lobby.isEmpty():
                del self.lobbies[lobbyId]
            return True
        return False

    def createLobby(self) -> str:
        id = self.getNewLobbyId()
        self.lobbies[id] = Lobby(id)
        return id

    def getNewLobbyId(self) -> str:
        while True:
            guess = random.randint(1000, 9999)
            if guess not in self.lobbies:
                return str(guess)

    def assignPlayerToLobby(self, lobbyId: str, playerId: str) -> bool:
        lobby = self.lobbies.get(lobbyId, None)
        player = self.players.get(playerId, None)
        print(lobbyId, playerId)
        if lobby and player and not lobby.isFull():
            lobby.addPlayer(player)
            player.lobbyId = lobby.id
            return True
        #print(lobby, player)
        return False

    def tryToStartGame(self, lobbyId:str) -> Game:
        lobby = self.lobbies.get(lobbyId)
        if not lobby:
            raise ValueError("Lobby does not exist")

        if not lobby.isFull():
            raise ValueError("Not enough player to start a Game")
        
        return lobby.startGame()

    def handleBid(self, playerId:str, lobbyId:str, bid:str) -> bool:
        #first try to get the game from the lobby obj if it exist
        lobby = self.lobbies.get(lobbyId)
        if not lobby:
            raise ValueError(f"{lobbyId} does not exist")

        if not lobby.game:
            raise ValueError(f"{lobbyId} has not started a game yet")
        
        try:
            lobby.game.makeBid(playerId, bid)
        except ValueError as e:
            raise e

        return lobby.game.isBiddingComplete() 
