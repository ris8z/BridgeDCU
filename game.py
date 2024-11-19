from round import Round
from typing import List
from player import Player
from bidPhase import Contract

class Game(object):

    def __init__(self, players: List[Player]):
        self.players = players
        self.currentRound: Round | None = None
        self.completedRounds: List[Round] = []

    def makeBid(self, playerId:str, bid:str):
        if not self.currentRound:
            raise ValueError("No round is running know start a new one")
        self.currentRound.makeBid(playerId, bid)

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

    def startNewRound(self):
        if self.currentRound and not self.currentRound.isRoundOver():
            raise ValueError("can not start a new round until the current round is finished")

        self.currentRound = Round(self.players)

    def endCurrentRound(self):
        if not self.currentRound or not self.currentRound.isRoundOver():
            raise ValueError("can not end the round before it is completed")

        #here we should calculate the points but not know not for me

        #add the round to the records
        self.completedRounds.append(self.currentRound)
        self.currentRound = None

    def isGameOver(self) -> bool:
        return len(self.completedRounds) == 1
