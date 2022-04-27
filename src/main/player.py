import random
from typing import List
from card import card

class player:
    def __init__(self) -> None:
        # setting up important stuff
        self.deck: List[card] = []
        self.deck_amount: int = 30
        self.hand: List[card] = []
        self.graveyard: List[card] = []
        self.selected_card: card = None

        self.create_deck()
        self.invoke_hand()

    def create_deck(self) -> None:
        # creates deck of 10 random cards
        self.deck = [card() for _ in range(self.deck_amount)]

    def invoke_hand(self) -> None:
        if (len(self.hand) == 3): return

        if (len(self.hand) == 0):
            # takes first 3 cards from deck
            self.hand = [self.deck[_] for _ in range(3)]
            del self.deck[0:3]
        else:
            # takes top card from deck
            self.hand.append(self.deck[0])
            del self.deck[0]

    def invoke_graveyard(self) -> None:
        if (self.selected_card == None): return
        
        self.graveyard.append(self.selected_card)
        self.selected_card = None

    def invoke_card(self, select: int) -> card:
        self.selected_card = self.hand[select]
        del self.hand[select]

        return (self.selected_card)

    def get_hand(self) -> List[card]:
        return (self.hand)

class bot(player):
    def __init__(self) -> None:
        # calling to player class
        super().__init__()

    def invoke_card(self) -> None:
        # gets random card from hand
        item: card = random.choice(self.hand)
        self.selected_card = item
        self.hand.remove(item)

        return (self.selected_card)