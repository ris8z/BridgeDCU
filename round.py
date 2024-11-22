from typing import List
from player import Player
from bidPhase import BidPhase
from Deck import Card, Deck


class Round(object):
    def __init__(self, players:List[Player]):
        self.bid_phase_flag = True 
        self.is_round_over = False
        self.players = players
        self.bidPhase = BidPhase(self.players)
        self.dealCards() # quando creamio un round le carte vanno distribuite subito

    # quando starti il nuovo round da le carte alla genete e la gente le riceve
    # poi inizia la fase di bid mo chilla dio cane
    def dealCards(self):
        d = Deck()
        for p in self.players:
            p.hand = d.deal(13)

    def isRoundOver(self) -> bool:
        return self.is_round_over

    def isBiddingOver(self) -> bool:
        return not self.bid_phase_flag

    def makeBid(self, playerId:str, bid:str) -> bool: # true if the bidding is done
        if self.isBiddingOver():
            raise ValueError("not possilbe to bid outside of the bidding time")

        result = self.bidPhase.makeBid(playerId, bid)

        if result:
            self.bid_phase_flag = False
            self.is_round_over = True #this bc for the moment the round is just the bidding phase
                                      #a littile step at time
            return True

        return False
