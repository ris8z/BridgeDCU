from typing import List
from Card import Card, Suits, Values
import random

class Deck:
    def __init__(self) -> None:
        self.deck: List[Card] = self.initDeck()
        self.shuffle()

    def initDeck(self) -> List[Card]:
        res: List[Card] = []
        for suit in Suits:
            for value in Values:
                res.append(Card(value=value, suit=suit))
        return res

    def shuffle(self) -> None:
        for i in range(len(self.deck)):
            p:int = random.randint(0, len(self.deck) - 1)
            self.deck[i], self.deck[p] = self.deck[p], self.deck[i]

    def deal(self, number = 0) -> List[Card]:
        if number > len(self.deck):
            return []

        res: List[Card] = []
        for _ in range(number):
            res.append(self.deck.pop())
        return res 

    def __str__(self) -> str:
        lines: List[str] = ["["]
        buffer: List[str] = []
        for card in self.deck:
            buffer.append(str(card))
            if len(buffer) == 13:
                lines.append(", ".join(buffer))
                buffer = []
        lines.append("]")
        return "\n".join(lines)
