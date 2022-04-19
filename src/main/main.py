def main() -> None:
    discord_bot: discord.Client = discord.Client()

    raw_user_pool: List[discord.Member] = []
    active_user_pool: List[discord.Member] = []

    # list of the lobby class for storage
    lobby_storage: List[lobby] = [lobby(0)]

    @discord_bot.event
    async def on_ready() -> None:
        print(f'logged {discord_bot.user}')
        # creating the embedded message
        on_ready_embed: discord.Embed = await get_on_ready(discord_bot)

        for i in CHANNELS:
            msg: discord.Message = await discord_bot.get_channel(int(i)).send(embed = on_ready_embed)

            for r, v in REACTION_CONVERSIONS.items():
                if v == 'lobby_create': await msg.add_reaction(r)

    @discord_bot.event
    async def on_raw_reaction_add(payload: discord.RawReactionActionEvent) -> None:
        user: discord.Member = payload.member
        emoji: discord.Emoji = payload.emoji
        channel: discord.Guild = discord_bot.get_channel(int(payload.channel_id))
        message: discord.Message = await channel.fetch_message(int(payload.message_id))

        # if not bot, or reaction is in pre-defined categories
        if (user == discord_bot.user or str(channel.category.id) not in CATEGORIES or user in active_user_pool): return

        if (REACTION_CONVERSIONS.get(str(emoji))) == 'lobby_create':
            raw_user_pool.append(user)

            if (len(raw_user_pool) < 2): return
            info_dict: Dict[str, Union[List[discord.Member], lobby]] = await globals()[f'on_{REACTION_CONVERSIONS.get(str(emoji))}'](
                bot = discord_bot, 
                msg = message,
                us = user,
                rup = raw_user_pool,
                ls = lobby_storage
            )

            # sets value returned from bot_methods
            for u_z in info_dict.get('users_to_remove_from_rup'):
                await message.remove_reaction(emoji, u_z)

            for u_y in info_dict.get('users_to_add_to_aup'):
                active_user_pool.append(u_y)

            lobby_storage.append(info_dict.get('new_lobby'))

            return

        await globals()[f'on_{REACTION_CONVERSIONS.get(str(emoji))}'](bot = discord_bot, msg = message, us = user)

    @discord_bot.event
    async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent) -> None:
        emoji: discord.Emoji = payload.emoji
        channel: discord.Guild = discord_bot.get_channel(int(payload.channel_id))
        message: discord.Message = await channel.fetch_message(int(payload.message_id))

        # if not bot, or reaction is in pre-defined categories
        if (payload.user_id == discord_bot.user.id or str(channel.category.id) not in CATEGORIES): return

        if (REACTION_CONVERSIONS.get(str(emoji))) == 'lobby_create':
            raw_user: discord.Member = None
            for u in raw_user_pool:
                if (u.id == payload.user_id): raw_user = u
            
            if (raw_user): raw_user_pool.remove(raw_user)

            return

    discord_bot.run(TOKEN)

if (__name__ == '__main__'):
    from bot_methods import *
    
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