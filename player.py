from typing import List
from Card import Card

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
        try:
            self.hand.remove(card)
            return card
        except:
            ValueError("You don't have this card")
        
