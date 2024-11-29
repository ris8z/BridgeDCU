from Deck import Card, Suits
from typing import Dict, List
from player import Player
from bidPhase import Contract

class Trick(object):
    def __init__(self, trump):
        self.trick: Dict[int, Card] = {}
        self.trump: Suits | None = trump 

    def winner(self) -> int:
        cardPlayedWithTrump = [x for x in self.trick.items() if x[1].suit == self.trump]

        if len(cardPlayedWithTrump) > 0:
            p, _ = max(cardPlayedWithTrump, key=lambda x:x[1])
        else:
            p, _ = max(self.trick.items(), key=lambda x:x[1])

        return p

    def toDict(self):
        return {
            "0": {"value": str(self.trick[0].value), "suite": str(self.trick[0].suit)},
            "1": {"value": str(self.trick[1].value), "suite": str(self.trick[1].suit)},
            "2": {"value": str(self.trick[2].value), "suite": str(self.trick[2].suit)}, 
            "3": {"value": str(self.trick[3].value), "suite": str(self.trick[3].suit)},
        }


class TrickPahse(object):
    def __init__(self, players, contract):
        self.players: List[Player] = players
        self.currentTrick: Trick | None = None 
        self.current_turn = 0
        self.contract: Contract = contract
        self.flag = False # flag if we are making playing the dummy turn to the author
                          # so after we need to shift the turn one before

    def startTrick(self, turn):
        if not(0 <= turn and turn <= 4):
            raise ValueError("Not a valid index for the turn must be between 0-4")

        if self.currentTrick is not None:
            raise ValueError("wait first that this trick finish to create another one")

        self.current_turn = turn
        self.currentTrick = Trick(self.contract.suit)
        self.flag = False

    def makePlay(self, playerId: str, card: Card):
        if playerId != self.players[self.current_turn].id:
            raise ValueError("Not the player's turn to play")

        if not self.currentTrick:
            raise ValueError("We are not in the trick phase")


        if self.flag:
            idx = (self.current_turn + 2) % 4
        else:
            idx = self.current_turn

        
        player = self.players[idx]
        player.playCard(card) #check if the player has this card and remove it form his hand


        print(f"{player} has played {card} into {player.lobbyId}, playerHand {player.hand}")

        self.currentTrick.trick[idx] = card

        
        print(self.currentTrick.trick)
        if len(self.currentTrick.trick) == 4:
            result = self.currentTrick
            self.currentTrick = None
            return result

        # we know that the first turn is never the dummy bc it has to be the one left
        # to the author of the contract
        # so know we can check for the dummy

        if self.flag == True:
            self.current_turn = (self.current_turn - 1) % 4
            self.flag = False
            return None

        if (self.current_turn + 1) == self.contract.dummy:
            self.current_turn = (self.current_turn + 3) % 4
            self.flag = True
        else:
            self.current_turn = (self.current_turn + 1) % 4

        return None
