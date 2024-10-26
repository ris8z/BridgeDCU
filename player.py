from typing import List


class Card:
    pass


class Player:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.lobbyId = ""
        self.hand: List[Card] = []

    def enterLobby(self, room_id):
        self.lobbyId = room_id

    def quitLobby(self):
        self.lobbyId = ""

    def getCard(self, card):
        self.hand.append(card)

    def playCard(self, card):
        if card in self.hand:
            self.hand.remove(card)
            return card
        return None
