from player import Player
from typing import List
from Card import Suits

class Contract:
    def __init__(self, value=0, suit=None, author=-1, dummy=-1):
        self.value: int = value
        self.suit: Suits | None = suit
        self.author: int = author  # the index of the player that made the bid
        self.dummy: int = dummy  # the index of dummy

    def to_dict(self):
        return {
            "value": self.value,
            "suit": str(self.suit),
            "author": self.author,
            "dummy": self.dummy
        }

class BidPhase:
    def __init__(self, players: List[Player]): 
        self.players = players
        self.contract = Contract()
        self.current_turn = 0
        self.pass_in_a_row = 0

    def makeBid(self, playerId: str, bid:str) -> bool:
        if playerId != self.players[self.current_turn].id:
            raise ValueError("Not the player's turn to bid")

        if bid.lower() == "pass":
            self.pass_in_a_row += 1
        else:
            self.pass_in_a_row = 0

            try:
                value, suit = bid.split(",")
            except ValueError:
                raise ValueError(f"Invalid bid format: '{bid}'. Expected 'value,suit'. Empty suit for no Trump")

            if self.contract.value != 0 and int(value) < self.contract.value:
                raise ValueError("Your bid must be greater than the last one")

            self.contract.value = int(value)
            self.contract.suit = Suits(suit) if suit else None
            print(f"only time the contract change wiht idx {self.current_turn}")
            self.contract.author = self.current_turn
            self.contract.dummy = (self.current_turn + 2) % 4

        self.current_turn = (self.current_turn + 1) % 4
        return self.pass_in_a_row == 3 and self.contract.value > 0 #it return wheather or not the bid phase is ended
