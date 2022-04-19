import discord
from typing import Dict, List, Union
from player import player
from lobby import lobby

REACTION_CONVERSIONS: Dict[str, str] = {
    '✅': 'lobby_create'
}

async def get_on_ready(bot: discord.Client) -> discord.Embed:
    # grabbing key from value
    reaction_emoji: str
    for r, v in REACTION_CONVERSIONS.items():
        if v == 'lobby_create': reaction_emoji = r

    # initializing embed message
    on_ready_embed: discord.Embed = discord.Embed(
        title = 'card jitsu', 
        description = 'a cracked up version of rock-paper-scissors',
        color = 0x5865F2
    )

    (
        on_ready_embed.set_thumbnail(
            url = 'https://cdn.discordapp.com/attachments/841102995218890772/964579410374189157/unknown.png'
        )
                
            .add_field(
                name = 'rules',
                value = '''
                    - fire beats snow
                    - snow beats water
                    - water beats fire

                    if the played cards are of the same type, the highest value wins, if the number are also matched, it is a tie and no cards are won

                    ***to win the match***: a player's won cards have the same card type in 3 different colors or a player's won cards have one of each type of card in the same color
                                
                    [*original rules*](https://clubpenguin.fandom.com/wiki/Card-Jitsu)
                ''',
                inline = False
            )

            .add_field(
                name = 'to play',
                value = f'''
                    {reaction_emoji} to create a lobby
                ''',
                inline = False
            )
    )

    return (on_ready_embed)

async def on_lobby_create(
        bot: discord.Client, 
        msg: discord.Message,
        us: discord.User,
        **kwargs) -> Dict[str, Union[List[discord.Member], lobby]]:
    if (kwargs.get('rup') is None or kwargs.get('ls') is None): return (None)

    # setting up values sent from main script
    raw_user_pool: List[discord.Member] = kwargs.get('rup')
    lobby_storage: List[lobby] = kwargs.get('ls')

    # getting first 2 users that reacted
    user_a: discord.Member = raw_user_pool[0]
    user_b: discord.Member = raw_user_pool[1]

    player_a: player = player()
    player_b: player = player()

    # setting up game data
    l_id: int = (list(lobby_storage)[-1].get().get('lobby_id') + 1)

    channel_a: discord.TextChannel = await msg.guild.create_text_channel(
        f'dojo-{l_id}a', 
        category = msg.channel.category
    )
    await channel_a.set_permissions(user_a, read_messages = True)

    channel_b: discord.TextChannel = await msg.guild.create_text_channel(
        f'dojo-{l_id}b', 
        category = msg.channel.category
    )
    await channel_b.set_permissions(user_b, read_messages = True)

    new_lobby = lobby(l_id, [channel_a, channel_b], {channel_a: user_a, channel_b: user_b}, {user_a: player_a, user_b: player_b})

    return({
        'users_to_remove_from_rup': [user_a, user_b],
        'users_to_add_to_aup': [user_a, user_b],
        'new_lobby': new_lobby
    })