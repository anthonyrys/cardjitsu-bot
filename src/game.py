from typing import List, Dict, Union

from src.card import card
from src.player import player, bot

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
    def __init__(self, player_one: player = None, player_two: player = None) -> None:
        # setting up game variables
        self.players: List[player] = [player_one, player_two]
        self.won_cards: Dict[player, List[card]] = {player_one: [], player_two: []}

    def check_round_condition(self) -> Union[None, player]:
        card_one: card = self.players[0].selected_card
        card_two: card = self.players[1].selected_card

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
            fire_num: int = 0
            snow_num: int = 0
            water_num: int = 0

            for c in cards:
                if (c.get().get('type') == 'fire'): fire_num += 1
                if (c.get().get('type') == 'snow'): snow_num += 1
                if (c.get().get('type') == 'water'): water_num += 1

            # filtering types with 3 or more of the same
            found_types: List[str] = []
            if (fire_num >= 3): found_types.append('fire')
            if (snow_num >= 3): found_types.append('snow')
            if (water_num >= 3): found_types.append('water')

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
            red_num: int = 0
            blue_num: int =  0
            yellow_num: int = 0
            green_num: int = 0
            orange_num: int = 0
            purple_num: int = 0

            for c in cards:
                if (c.get().get('color') == 'red'): red_num += 1
                if (c.get().get('color') == 'blue'): blue_num += 1
                if (c.get().get('color') == 'yellow'): yellow_num += 1
                if (c.get().get('color') == 'green'): green_num += 1
                if (c.get().get('color') == 'orange'): orange_num += 1
                if (c.get().get('color') == 'purple'): purple_num += 1

            # filtering colors with 3 or more of the same
            found_colors: List[str] = []
            if (red_num >= 3): found_types.append('red')
            if (blue_num >= 3): found_types.append('blue')
            if (yellow_num >= 3): found_types.append('yellow')
            if (green_num >= 3): found_types.append('green')
            if (orange_num >= 3): found_types.append('orange')
            if (purple_num >= 3): found_types.append('purple')

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