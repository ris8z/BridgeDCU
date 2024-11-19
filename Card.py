from enum import Enum

class Suits(Enum):
    CLUB = "C"
    HEART = "H"
    SPADES = "S"
    DIAMOND = "D"

class Values(Enum):
    ACE = "A"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"

    def __lt__(self, other):
        if not isinstance(other, Values):
            return NotImplemented
        priority = {
            "A":13,
            "2":1,
            "3":2,
            "4":3,
            "5":4,
            "6":5,
            "7":6,
            "8":7,
            "9":8,
            "10":9,
            "J":10,
            "Q":11,
            "K":12,
        }
        return priority[self.value] < priority[other.value]

    def __eq__(self, other):
        if not isinstance(other, Values):
            return NotImplemented
        return self.value == other.value

class Card:
    def __init__(self, value: Values, suit: Suits) -> None:
        self.value = value
        self.suit = suit 

    def __lt__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.value < other.value

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"{self.value.value}{self.suit.value}"
    
    def __repr__(self) -> str:
        return self.__str__()
