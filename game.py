from round import Round
from typing import List, Dict
from player import Player
from bidPhase import Contract
from Card import Card
from trickPhase import Trick

class Game(object):

    def __init__(self, players: List[Player]):
        self.MAX_ROUND_NUMBERS = 2
        self.players = players
        self.currentRound: Round | None = None
        self.completedRounds: List[Round] = []
        self.points: Dict[int, int] = {x:0 for x in range(4)}

    def makeBid(self, playerId:str, bid:str):
        if not self.currentRound:
            raise ValueError("No round is running know start a new one")
        self.currentRound.makeBid(playerId, bid)

    def makePlay(self, playerId:str, card:Card):
        if not self.currentRound:
            raise ValueError("No round is running know start a new one")

        if not self.currentRound.makePlay(playerId, card):
            return False 

        return True 
       
    def isBiddingComplete(self) -> bool:
        if not self.currentRound:
            raise ValueError("No round is running know start a new one")
        return self.currentRound.isBiddingOver()

    def getContract(self) -> Contract: 
        if not self.currentRound:
            raise ValueError("No round running now")
        if not self.currentRound.isBiddingOver():
            raise ValueError("bidding not yet completed")
        return self.currentRound.bidPhase.contract

    def getLastTrick(self) -> Trick:
        if not self.currentRound:
            raise ValueError("No round running now")       
        if not self.currentRound.trickPhase:
            raise ValueError("Not in the trick phase")       

        return self.currentRound.tricks[-1]

    def startNewRound(self):
        if self.currentRound and not self.currentRound.isRoundOver():
            raise ValueError("can not start a new round until the current round is finished")

        self.currentRound = Round(self.players)

    def endCurrentRound(self):
        if not self.currentRound or not self.currentRound.isRoundOver():
            raise ValueError("can not end the round before it is completed")

        #here we should calculate the points 
        for trick in self.currentRound.tricks:
            idx = trick.winner()
            self.points[idx] = self.points.get(idx, 0) + 1 

        #add the round to the records
        self.completedRounds.append(self.currentRound)
        self.currentRound = None

    def isGameOver(self) -> bool:
        return len(self.completedRounds) == self.MAX_ROUND_NUMBERS 
