from typing import List
from player import Player
from bidPhase import BidPhase
from trickPhase import Trick, TrickPahse
from Deck import Card, Deck


class Round(object):
    def __init__(self, players: List[Player]):
        self.MAX_NUMBER_TRICKS = 3
        self.bid_phase_flag = True
        self.trick_phase_flag = False
        self.is_round_over = False
        self.players = players
        self.bidPhase = BidPhase(self.players)
        self.trickPhase: TrickPahse | None = None
        self.tricks: List[Trick] = []
        self.dealCards()  # quando creamio un round le carte vanno distribuite subito

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

    def isTrickPhaseOn(self) -> bool:
        return self.trick_phase_flag

    def makeBid(self, playerId: str, bid: str) -> bool:  # true if the bidding is done
        if self.isBiddingOver():
            raise ValueError("not possilbe to bid outside of the bidding time")

        result = self.bidPhase.makeBid(playerId, bid)

        if result:
            self.bid_phase_flag = False

            self.trickPhase = TrickPahse(self.players, self.bidPhase.contract)
            self.trickPhase.startTrick(self.bidPhase.getFirstTurn())

            self.trick_phase_flag = True
            return True

        return False

    def makePlay(self, playerId: str, card: Card):
        if not self.isTrickPhaseOn() or not self.trickPhase:
            raise ValueError("you can not play a card outside of tick phase")
        
        result = self.trickPhase.makePlay(playerId, card)
        if result:
            self.tricks.append(result)
            print(f"A new trick has been added to the round {self.tricks}")

            if len(self.tricks) >= self.MAX_NUMBER_TRICKS:
                self.is_round_over = True
            else:
                # we should start another trick, here start the winner of the last one
                # if the winner is the dummy we need to pass the position of his teamate
                winner = self.tricks[-1].winner()
                if winner == self.bidPhase.contract.dummy:
                    idx = (winner + 2) % 4
                else:
                    idx = winner
                self.trickPhase.startTrick(idx)

        return result 
