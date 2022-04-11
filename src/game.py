from card import card
from player import player, bot
from typing import List, Dict, Union

'''
    Original rules: https://clubpenguin.fandom.com/wiki/Card-Jitsu#Winning

    Round win condition:
        - fire beats snow
        - snow beats water
        - water beats fire

        if the played cards are of the same type, the highest value wins
        ^ if the number are also matched, it is a tie and no cards are won

    Match win conditions:
        1: if player's won cards have the same card type in 3 different colors
        2: if player's won cards have one of each type of card in the same color
'''

class game:
    def __init__(self, player_one: player, player_two: player) -> None:
        # setting up game variables
        self.players: List[player] = [player_one, player_two]
        self.won_cards: Dict[player, List[card]] = {player_one: [], player_two: []}

        self.run()

    def run(self) -> None:
        while (self.check_match_condition() is None):
            pass

    def check_round_condition(self) -> Union[None, player]:
        card_one: card = self.players[0].invoke_card()
        card_two: card = self.players[1].invoke_card()

        # a bunch of if-else statements for checking round conditions
        if (card_one.get().get('type') == 'fire'):
            if (card_two.get().get('type') == 'snow'): return (self.players[0])
            elif (card_two.get().get('type') == 'water'): return (self.players[1])
            elif (card_two.get().get('type') == 'fire'):
                if (card_one.get().get('rank') > card_two.get().get('rank')): return (self.players[0])
                elif (card_one.get().get('rank') < card_two.get().get('rank')): return (self.players[1])
                else: return (None)

        if (card_one.get().get('type') == 'snow'):
            if (card_two.get().get('type') == 'water'): return (self.players[0])
            elif (card_two.get().get('type') == 'fire'): return (self.players[1])
            elif (card_two.get().get('type') == 'snow'):
                if (card_one.get().get('rank') > card_two.get().get('rank')): return (self.players[0])
                elif (card_one.get().get('rank') < card_two.get().get('rank')): return (self.players[1])
                else: return (None)

        if (card_one.get().get('type') == 'water'):
            if (card_two.get().get('type') == 'fire'): return (self.players[0])
            if (card_two.get().get('type') == 'snow'): return (self.players[1])
            elif (card_two.get().get('type') == 'water'):
                if (card_one.get().get('rank') > card_two.get().get('rank')): return (self.players[0])
                elif (card_one.get().get('rank') < card_two.get().get('rank')): return (self.players[1])
                else: return (None)


    def check_match_condition(self) -> Union[None, player]:
        for p in self.players:
            cards: List[card] = self.won_cards.get(p)

            # checking condition 1
            condition_types: Dict[str, int] = {
                'fire': 0,
                'snow': 0,
                'water': 0
            }

            for c in cards:
                if (c.get().get('type') == 'fire'): condition_types['fire'] += 1
                if (c.get().get('type') == 'snow'): condition_types['snow'] += 1
                if (c.get().get('type') == 'snow'): condition_types['water'] += 1

            # filtering types with 3 or more of the same
            found_types: List[str] = []
            for k, v in condition_types.items():
                if (v >= 3): 
                    found_types.append(k)

            if (found_types):
                validation_list: List[card] = []
                for c in cards:
                    if (c.get().get('type') == found_types[0]): validation_list.append(c)

                # filtering types with 3 different colors
                inner_colors: List[str] = []
                for vl in validation_list:
                    if vl.get().get('color') not in inner_colors: inner_colors.append(vl.get().get('color'))
                
                if (len(inner_colors) >= 3): return (p)


            # checking condition 2
            condition_colors: Dict[str, int] = {
                'red': 0,
                'blue': 0,
                'yellow': 0,
                'green': 0,
                'orange': 0,
                'purple': 0
            }

            for c in cards:
                if (c.get().get('color') == 'red'): condition_colors['red'] += 1
                if (c.get().get('color') == 'blue'): condition_colors['blue'] += 1
                if (c.get().get('color') == 'yellow'): condition_colors['yellow'] += 1
                if (c.get().get('color') == 'green'): condition_colors['green'] += 1
                if (c.get().get('color') == 'orange'): condition_colors['orange'] += 1
                if (c.get().get('color') == 'purple'): condition_colors['purple'] += 1

            # filtering colors with 3 or more of the same
            found_colors: List[str] = []
            for k, v in condition_colors.items():
                if (v >= 3): 
                    found_colors.append(k)

            if (found_colors):
                validation_list: List[card] = []
                for c in cards:
                    if (c.get().get('color') == found_colors[0]): validation_list.append(c)

                # filtering colors with 3 different types
                inner_types: List[str] = []
                for vl in validation_list:
                    if vl.get().get('type') not in inner_types: inner_types.append(vl.get().get('type'))
                
                if (len(inner_types) >= 3): return (p)

        return (None)

    def compare_cards(self) -> player:
        pass
