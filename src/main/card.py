import random
from dataclasses import dataclass
from typing import Dict, List, Union

# global variables
COLORS: List[str] = ['red', 'blue', 'yellow', 'green', 'orange', 'purple']
TYPES: List[str] = ['fire', 'water', 'snow']

@dataclass
class card:
    # default object variables
    color: str = 'green'
    type: str = 'ice'
    rank: int = 5
    
    # randomizer
    def __post_init__(self) -> None:   
        self.color = random.choice(COLORS)
        self.type = random.choice(TYPES)
        self.rank = round(random.random() * 10 + 2)

    # return card info
    def get(self) -> Dict[str, Union[int, str]]:
        return({
            'color': self.color, 
            'type': self.type,
            'rank': self.rank
        })