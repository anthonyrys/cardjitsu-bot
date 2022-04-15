import discord
from typing import List

def main() -> None:
    bot: discord = discord.Client()

    # init
    @bot.event
    async def on_ready() -> None:
        print(f'logged {bot.user}')

        # info message
        info_msg: discord = discord.Embed(
            title = 'card jitsu', 
            description = 'a cracked up version of rock-paper-scissors',
            color = 0x5865F2
        )

        (
            info_msg.set_thumbnail(
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
                        ✅ to play with a bot
                        ~~☑️ to get paired up against another player~~
                    ''',
                    inline = False
                )
        )

        for i in ID_CHANNELS:
            msg: discord = await bot.get_channel(int(i)).send(embed = info_msg)
            await msg.add_reaction('✅')
            await msg.add_reaction('☑️')

    @bot.event
    async def on_reaction_add(reaction: discord, user: discord) -> None:
        if (user != bot.user):
            if (str(reaction.message.channel) not in STR_CHANNELS): return

            # play with bot
            if (reaction.emoji == '✅'):
                await reaction.remove(user)

            # play with player // tbd
            if (reaction.emoji == '☑️'):
                await reaction.remove(user)

    # run
    bot.run(TOKEN)

if (__name__ == '__main__'):
    TOKEN: str
    
    # channel in which the bot is allowed to post
    ID_CHANNELS: List[int]
    STR_CHANNELS: List[str]

    # getting token
    with open('src/main/data/token.txt', 'r') as t:
        TOKEN = t.readline()

    # getting writable servers
    with open('src/main/data/channels_id.txt', 'r') as c:
        ID_CHANNELS = c.readlines()

    with open('src/main/data/channels_str.txt', 'r') as c:
        STR_CHANNELS = c.readlines()

    main()