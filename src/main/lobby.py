import discord
from dataclasses import dataclass
from typing import Dict, List, Union
from player import player
from game import game

@dataclass
class lobby:
    # lobby variables
    lobby_id: int
    channels: List[discord.TextChannel]
    user_channels: Dict[discord.TextChannel, discord.Member]
    user_players: Dict[discord.Member, player]

    def __init__(
            self, 
            l_id: int = None, 
            chnls: List[discord.TextChannel] = None, 
            u_chnls: Dict[discord.TextChannel, discord.Member] = None,
            u_plrs: Dict[discord.Member, player] = None) -> None:
        self.lobby_id = l_id 
        self.channels = chnls
        self.user_channels = u_chnls
        self.user_players = u_plrs

    def set_game(self, gme: game):
        pass

    def get(self) -> Dict[str, Union[int, Dict[Union[discord.TextChannel, discord.Member], Union[discord.Member, player]]]]:
        return({
            'lobby_id': self.lobby_id,
            'channels': self.channels,
            'user_channels': self.user_channels,
            'user_players': self.user_players
        })