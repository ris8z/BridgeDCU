from typing import List
from player import Player
from flask_socketio import join_room, leave_room, emit


class Lobby:
    def __init__(self, id: str):
        self.id = id
        self.players: List[Player] = []

    def isFull(self) -> bool:
        return len(self.players) == 4

    def isEmpty(self) -> bool:
        return len(self.players) == 0

    def addPlayer(self, player: Player) -> bool:
        if len(self.players) < 4:
            self.players.append(player)
            join_room(self.id, sid=player.id)
            return True
        return False

    def removePlayer(self, player: Player) -> bool:
        if player in self.players:
            self.players.remove(player)
            leave_room(self.id, sid=player.id)
            return True
        return False

    def broadcastMassage(self, eventName, data):
        emit(eventName, data, to=self.id)
