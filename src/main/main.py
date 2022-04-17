import discord
from typing import List
from bot_methods import get_on_ready

def main() -> None:
    discord_bot: discord.client.Client = discord.Client()

    @discord_bot.event
    async def on_ready() -> None:
        print(f'logged {discord_bot.user}')
        # creating the embedded message
        on_ready_embed: discord.embeds.Embed = await get_on_ready(discord_bot)

        for i in CHANNELS:
            msg: discord.message.Message = await discord_bot.get_channel(int(i)).send(embed = on_ready_embed)
            await msg.add_reaction('✅')

    @discord_bot.event
    async def on_reaction_add(reaction: discord.reaction.Reaction, user: discord.user.User) -> None:
        # if not bot, or reaction is in pre-defined categories
        if (user == discord_bot.user or str(reaction.message.channel.category.id) not in CATEGORIES): return
        
        await reaction.remove(user)

    discord_bot.run(TOKEN)

if (__name__ == '__main__'):
    TOKEN: str

    CHANNELS: List[str]
    CATEGORIES: List[str]

    # getting token
    with open('src/main/data/token.txt', 'r') as t:
        TOKEN = t.readline()

    # getting writable servers & channels
    with open('src/main/data/channels.txt', 'r') as c:
        CHANNELS = c.readlines()

    with open('src/main/data/categories.txt', 'r') as c:
        CATEGORIES = c.readlines()

    main()