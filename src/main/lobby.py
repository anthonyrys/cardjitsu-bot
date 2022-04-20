import discord
from dataclasses import dataclass
from typing import Dict, List, Union
from player import player
from game import game

@dataclass
class lobby:
    # lobby variables
    lobby_id: int
    lobby_check: int
    lobby_game: game
    users: List[discord.Member]
    channels: List[discord.TextChannel]
    user_channels: Dict[discord.TextChannel, discord.Member]
    user_players: Dict[discord.Member, player]
    current_messages: List[discord.Message]

    def __init__(
            self, 
            l_id: int = None, 
            users: List[discord.Member] = None,
            chnls: List[discord.TextChannel] = None, 
            u_chnls: Dict[discord.TextChannel, discord.Member] = None,
            u_plrs: Dict[discord.Member, player] = None) -> None:
        self.lobby_id = l_id 
        self.lobby_check = 0
        self.lobby_game = None
        self.users = users
        self.channels = chnls
        self.user_channels = u_chnls
        self.user_players = u_plrs
        self.current_messages = None

    def set_game(self, gme: game) -> None:
        self.lobby_game = gme

    def get(self) -> Dict[str, Union[int, Dict[Union[discord.TextChannel, discord.Member], Union[discord.Member, player]]]]:
        return({
            'lobby_id': self.lobby_id,
            'lobby_check': self.lobby_check,
            'lobby_game': self.lobby_game,
            'users': self.users,
            'channels': self.channels,
            'user_channels': self.user_channels,
            'user_players': self.user_players,
            'current_messages': self.current_messages
        })