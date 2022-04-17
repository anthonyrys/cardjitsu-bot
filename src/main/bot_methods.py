import discord

async def get_on_ready(bot: discord.client.Client) -> discord.embeds.Embed:
    # initializing embed message
    on_ready_embed: discord = discord.Embed(
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
                value = '''
                    ✅ to create a lobby
                ''',
                inline = False
            )
    )

    return (on_ready_embed)