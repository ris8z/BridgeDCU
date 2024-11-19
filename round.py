from typing import List
from player import Player
from bidPhase import BidPhase


class Round(object):
    def __init__(self, players:List[Player]):
        self.bid_phase_flag = True 
        self.is_round_over = False
        self.players = players
        self.bidPhase = BidPhase(self.players)

    def isRoundOver(self) -> bool:
        return self.is_round_over

    def isBiddingOver(self) -> bool:
        return not self.bid_phase_flag

    def makeBid(self, playerId:str, bid:str) -> bool: # true if the bidding is done
        result = self.bidPhase.makeBid(playerId, bid)
        if result:
            self.bid_phase_flag = False
            self.is_round_over = True
            return True
        return False
