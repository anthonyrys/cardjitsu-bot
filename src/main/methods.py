import discord
import asyncio
from typing import Dict, List, Union
from card import card, CARD_CONVERSIONS
from player import player, bot
from lobby import lobby
from game import game

REACTION_CONVERSIONS: Dict[Union[str, List[str]], str] = {
    '✅': 'lobby_create',
    '☑️': 'lobby_create_solo',
    '👍': 'lobby_confirm',

    '1️⃣': 'option_pick_one',
    '2️⃣': 'option_pick_two',
    '3️⃣': 'option_pick_three'
}

# global variables used in main script
lobby_storage: List[lobby] = [lobby(0)]
raw_user_pool: List[discord.Member] = []
active_user_pool: List[discord.Member] = []

async def get_on_ready(bot: discord.Client) -> discord.Embed:
    # grabbing key from value
    reaction_emoji: str
    reaction_emoji_b: str

    for r, v in REACTION_CONVERSIONS.items():
        if v == 'lobby_create': reaction_emoji = r
        if v == 'lobby_create_solo': reaction_emoji_b = r

    # initializing embed message
    on_ready_embed: discord.Embed = discord.Embed(
        title = 'card jitsu', 
        description = 'an abridged version of rock-paper-scissors',
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
                    {reaction_emoji} to create a multiplayer lobby
                    {reaction_emoji_b} to create a singleplayer lobby
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
    
    reaction_emoji: str
    for r, v in REACTION_CONVERSIONS.items():
        if v == 'lobby_confirm': reaction_emoji = r

    on_create_embed: discord.Embed = discord.Embed(
        title = 'confirmation', 
        description = f'{reaction_emoji} to ready',
        color = 0x5865F2
    )

    # channel a    
    channel_a: discord.TextChannel = await msg.guild.create_text_channel(
        f'dojo-{l_id}a', 
        category = msg.channel.category
    )
    await channel_a.set_permissions(user_a, read_messages = True)
    msg_a: discord.Message = await channel_a.send(embed = on_create_embed)
    await msg_a.add_reaction(reaction_emoji)

    # channel b
    channel_b: discord.TextChannel = await msg.guild.create_text_channel(
        f'dojo-{l_id}b', 
        category = msg.channel.category
    )
    await channel_b.set_permissions(user_b, read_messages = True)
    msg_b: discord.Message = await channel_b.send(embed = on_create_embed)
    await msg_b.add_reaction(reaction_emoji)

    new_lobby = lobby(
        l_id, 
        [user_a, user_b], 
        [channel_a, channel_b], 
        {channel_a: user_a, channel_b: user_b}, 
        {user_a: player_a, user_b: player_b}
    )
    new_lobby.current_messages = [msg_a, msg_b]

    return({
        'users_to_remove_from_rup': [user_a, user_b],
        'users_to_add_to_aup': [user_a, user_b],
        'new_lobby': new_lobby
    })

async def on_lobby_create_solo(
        d_bot: discord.Client, 
        msg: discord.Message,
        us: discord.User,
        **kwargs) -> Dict[str, Union[List[discord.Member], lobby]]:
    if (kwargs.get('ls') is None): return (None)

    user_a: discord.Member = us
    user_b: discord.Member = d_bot.user

    player_a: player = player()
    player_b: player = bot()

    # setting up game data
    l_id: int = (list(lobby_storage)[-1].get().get('lobby_id') + 1)

    reaction_emoji: str
    for r, v in REACTION_CONVERSIONS.items():
        if v == 'lobby_confirm': reaction_emoji = r

    on_create_embed: discord.Embed = discord.Embed(
        title = 'confirmation', 
        description = f'{reaction_emoji} to ready',
        color = 0x5865F2
    )

    channel: discord.TextChannel = await msg.guild.create_text_channel(
        f'dojo-{l_id}a', 
        category = msg.channel.category
    )

    await channel.set_permissions(user_a, read_messages = True)
    msg_a: discord.Message = await channel.send(embed = on_create_embed)
    await msg_a.add_reaction(reaction_emoji)

    new_lobby = lobby(
        l_id, 
        [user_a, user_b], 
        [channel], 
        {channel: user_a}, 
        {user_a: player_a, user_b: player_b},
        1
    )
    new_lobby.current_messages = [msg_a]

    return({
        'user_to_remove_from_rup': user_a,
        'user_to_add_to_aup': user_a,
        'new_lobby': new_lobby
    })

async def on_lobby_confirm(
        bot: discord.Client, 
        msg: discord.Message,
        us: discord.User,
        **kwargs) -> None:
    if (kwargs.get('ls') is None): return (None)

    # setting up values sent from main script
    lobby_storage: List[lobby] = kwargs.get('ls')
    selected_lobby: lobby
    user_a: discord.Member
    user_b: discord.Member

    # grabbing lobby from reacted player
    for l in lobby_storage:
        user_list: list[discord.Member] = l.get().get('users')
        if (user_list is None): continue

        if (us in user_list): 
            selected_lobby = l
            user_a = user_list[0]
            user_b = user_list[1]

    if (selected_lobby.lobby_type == 0):
        # ensuring that both players are ready
        selected_lobby.lobby_check += 1 
        if (selected_lobby.get().get('lobby_check')) != 2: return

    # clearing confirm message
    for m in selected_lobby.get().get('current_messages'):
        await m.delete()
    selected_lobby.current_messages.clear()

    # starting the game
    new_game: game = game(
        selected_lobby.get().get('user_players').get(user_a),
        selected_lobby.get().get('user_players').get(user_b)
    )

    selected_lobby.set_game(new_game)
    await display_options(selected_lobby)

async def on_lobby_deconfirm(
    bot: discord.Client, 
    msg: discord.Message,
    usi: int,
    **kwargs) -> None:
    if (kwargs.get('ls') is None): return (None)

    # setting up values sent from main script
    lobby_storage: List[lobby] = kwargs.get('ls')
    selected_lobby: lobby
    us: discord.Member = await bot.fetch_user(usi)

    # grabbing lobby from unreacted player
    for l in lobby_storage:
        user_list: list[discord.Member] = l.get().get('users')
        if (user_list is None): continue

        if us in user_list:
            selected_lobby = l
    
    selected_lobby.lobby_check -= 1

async def clear_lobby(lb: lobby) -> None:
    for chnls in lb.channels: await chnls.delete()
    for usrs in lb.users: 
        if usrs in active_user_pool: active_user_pool.remove(usrs)
    lobby_storage.remove(lb)
    del lb

async def display_options(lb: lobby) -> None:
    lb_game = lb.get().get('lobby_game')

    # creating message for user in lobby (singleplayer)
    if (lb.lobby_type == 1):
        u: discord.Member = lb.users[0]
        channel: discord.TextChannel

        for chn, user in lb.get().get('user_channels').items():
            if user == u: channel = chn

        plr: player = lb.get().get('user_players').get(u)

        # creating embeds
        on_winning_cards: discord.Embed = discord.Embed(
                title = 'winning cards',
                color = 0xDDDDDD
        )

        on_displayed_options: discord.Embed = discord.Embed(
            title = 'your hand',
            color = 0xDDDDDD
        )

        # displaying winning cards
        for game_plr, crd_list in (lb_game.won_cards.items()):
            game_user: discord.Member
            for dp, lp in lb.get().get('user_players').items():
                if lp == game_plr: game_user = dp

            crd_string: str = (f'')
                
            if (crd_list):
                for new_crd in crd_list:
                    type: str = CARD_CONVERSIONS.get(new_crd.get().get('type'))
                    color: str = CARD_CONVERSIONS.get(new_crd.get().get('color'))
                    rank: str = CARD_CONVERSIONS.get(new_crd.get().get('rank'))

                    new_str: str = f'''{type} {color} {rank}◾◾'''
                    crd_string += new_str

            else: 
                crd_string: str = (f'◾')

            on_winning_cards.add_field(
                name = f'{crd_string}',
                value = f'{game_user.mention}',
                inline = False
            )

        # creating emojis
        pick_one: str
        pick_two: str
        pick_three: str

        for r, v in REACTION_CONVERSIONS.items():
            if v == 'option_pick_one': pick_one = r

        for r, v in REACTION_CONVERSIONS.items():
            if v == 'option_pick_two': pick_two = r

        for r, v in REACTION_CONVERSIONS.items():
            if v == 'option_pick_three': pick_three = r

        # displaying cards in players hand
        for count, crd in enumerate(plr.get_hand()):
            type: str = CARD_CONVERSIONS.get(crd.get().get('type'))
            color: str = CARD_CONVERSIONS.get(crd.get().get('color'))
            rank: str = CARD_CONVERSIONS.get(crd.get().get('rank'))
            on_displayed_options.add_field(
                name = (f'{count + 1}'),
                value = (f'''
                {type} {color} {rank}
                '''
                ),
                inline = False
            )

        # finalizing
        cards_msg: discord.Message = await channel.send(embed = on_winning_cards)
        option_msg: discord.Message = await channel.send(embed = on_displayed_options)
        await option_msg.add_reaction(pick_one)
        await option_msg.add_reaction(pick_two)
        await option_msg.add_reaction(pick_three)

        lb.current_messages.append(cards_msg)
        lb.current_messages.append(option_msg)

    else:
        # creating message for each user in lobby (multiplayer)
        for u in lb.get().get('users'):
            channel: discord.TextChannel
            for chn, user in lb.get().get('user_channels').items():
                if user == u: channel = chn

            plr: player = lb.get().get('user_players').get(u)
        
            # creating embeds
            on_winning_cards: discord.Embed = discord.Embed(
                title = 'winning cards',
                color = 0xDDDDDD
            )

            on_displayed_options: discord.Embed = discord.Embed(
                title = 'your hand',
                color = 0xDDDDDD
            )

            # displaying winning cards
            for game_plr, crd_list in (lb_game.won_cards.items()):
                game_user: discord.Member
                for dp, lp in lb.get().get('user_players').items():
                    if lp == game_plr: game_user = dp

                crd_string: str = (f'')
                
                if (crd_list):
                    for new_crd in crd_list:
                        type: str = CARD_CONVERSIONS.get(new_crd.get().get('type'))
                        color: str = CARD_CONVERSIONS.get(new_crd.get().get('color'))
                        rank: str = CARD_CONVERSIONS.get(new_crd.get().get('rank'))

                        new_str: str = f'''{type} {color} {rank}◾◾'''
                        crd_string += new_str

                else: 
                    crd_string: str = (f'◾')

                on_winning_cards.add_field(
                    name = f'{crd_string}',
                    value = f'{game_user.mention}',
                    inline = False
                )

            # creating emojis
            pick_one: str
            pick_two: str
            pick_three: str

            for r, v in REACTION_CONVERSIONS.items():
                if v == 'option_pick_one': pick_one = r

            for r, v in REACTION_CONVERSIONS.items():
                if v == 'option_pick_two': pick_two = r

            for r, v in REACTION_CONVERSIONS.items():
                if v == 'option_pick_three': pick_three = r

            # displaying cards in players hand
            for count, crd in enumerate(plr.get_hand()):
                type: str = CARD_CONVERSIONS.get(crd.get().get('type'))
                color: str = CARD_CONVERSIONS.get(crd.get().get('color'))
                rank: str = CARD_CONVERSIONS.get(crd.get().get('rank'))
                on_displayed_options.add_field(
                    name = (f'{count + 1}'),
                    value = (f'''
                    {type} {color} {rank}
                    '''
                    ),
                    inline = False
                )

            # finalizing
            cards_msg: discord.Message = await channel.send(embed = on_winning_cards)
            option_msg: discord.Message = await channel.send(embed = on_displayed_options)
            await option_msg.add_reaction(pick_one)
            await option_msg.add_reaction(pick_two)
            await option_msg.add_reaction(pick_three)

            lb.current_messages.append(cards_msg)
            lb.current_messages.append(option_msg)

async def on_option_pick(
        bot: discord.Client, 
        msg: discord.Message,
        us: discord.User,
        num: int,
        **kwargs) -> None:
    if (kwargs.get('ls') is None): return (None)

    # setting up values sent from main script
    lobby_storage: List[lobby] = kwargs.get('ls')
    selected_lobby: lobby
    channel: discord.TextChannel

    for l in lobby_storage:
        user_list: list[discord.Member] = l.get().get('users')
        if (user_list is None): continue

        if (us in user_list): 
            selected_lobby = l

    if (us != selected_lobby.user_channels.get(msg.channel)): return
    
    for chn, user in selected_lobby.get().get('user_channels').items():
        if user == us: channel = chn

    if (selected_lobby is None): return

    lobby_players: List[player] = list(selected_lobby.get().get('user_players').values())

    # invoking selected card
    user_player = selected_lobby.get().get('user_players').get(us)
    if (user_player.selected_card != None): return

    user_player.invoke_card(num)

    selected_lobby.current_messages.remove(msg)
    await msg.delete()

    type: str = CARD_CONVERSIONS.get(user_player.selected_card.get().get('type'))
    color: str = CARD_CONVERSIONS.get(user_player.selected_card.get().get('color'))
    rank: str = CARD_CONVERSIONS.get(user_player.selected_card.get().get('rank'))
    on_inputed_option: discord.Embed = discord.Embed(
            title = 'your chosen card',
            description = f'{type} {color} {rank}',
            color = 0xDDDDDD
    )
    input_msg: discord.Message = await channel.send(embed = on_inputed_option)  
    selected_lobby.current_messages.append(input_msg)

    if (selected_lobby.lobby_type == 1):
        selected_lobby.user_players.get(selected_lobby.users[1]).invoke_card()

        for msgs in selected_lobby.current_messages: await msgs.delete()
        selected_lobby.current_messages.clear()

        # checking for round winner
        winning_round_player: player = selected_lobby.lobby_game.check_round_condition()
        winning_round_user: discord.Member

        for usr, plr in selected_lobby.get().get('user_players').items():
            if winning_round_player == plr: winning_round_user = usr

        if (winning_round_player):
            losing_round_player: player 
            for plrs in selected_lobby.lobby_game.players:
                if plrs != winning_round_player: losing_round_player = plrs

            w_type: str = CARD_CONVERSIONS.get(winning_round_player.selected_card.get().get('type'))
            w_color: str = CARD_CONVERSIONS.get(winning_round_player.selected_card.get().get('color'))
            w_rank: str = CARD_CONVERSIONS.get(winning_round_player.selected_card.get().get('rank'))

            l_type: str = CARD_CONVERSIONS.get(losing_round_player.selected_card.get().get('type'))
            l_color: str = CARD_CONVERSIONS.get(losing_round_player.selected_card.get().get('color'))
            l_rank: str = CARD_CONVERSIONS.get(losing_round_player.selected_card.get().get('rank'))

            on_winning_player: discord.Embed = discord.Embed(
                title = 'results',
                description = f'{winning_round_user.mention} won the round',
                color = 0xDDDDDD
            )
            
            on_winning_player.add_field(
                name = 'chosen cards',
                value = f'''{w_type} {w_color} {w_rank}◾vs◾{l_type} {l_color} {l_rank}''',
                inline = False
            )

            for txtchnls in list(selected_lobby.user_channels.keys()):
                round_winning_msg: discord.TextChannel = await txtchnls.send(embed = on_winning_player)
                selected_lobby.current_messages.append(round_winning_msg)

            # updating values
            selected_lobby.lobby_game.won_cards.get(winning_round_player).append(winning_round_player.selected_card)

            for d_plrs in selected_lobby.lobby_game.players:
                d_plrs.invoke_graveyard()
                d_plrs.invoke_hand()

        elif (winning_round_player is None):
            a_type: str = CARD_CONVERSIONS.get(selected_lobby.lobby_game.players[0].selected_card.get().get('type'))
            a_color: str = CARD_CONVERSIONS.get(selected_lobby.lobby_game.players[0].selected_card.get().get('color'))
            a_rank: str = CARD_CONVERSIONS.get(selected_lobby.lobby_game.players[0].selected_card.get().get('rank'))

            b_type: str = CARD_CONVERSIONS.get(selected_lobby.lobby_game.players[1].selected_card.get().get('type'))
            b_color: str = CARD_CONVERSIONS.get(selected_lobby.lobby_game.players[1].selected_card.get().get('color'))
            b_rank: str = CARD_CONVERSIONS.get(selected_lobby.lobby_game.players[1].selected_card.get().get('rank'))


            on_tie: discord.Embed = discord.Embed(
                title = 'results',
                description = f'neither player won the round',
                color = 0xDDDDDD
            )

            on_tie.add_field(
                name = 'chosen cards',
                value = f'''{a_type} {a_color} {a_rank}◾vs◾{b_type} {b_color} {b_rank}''',
                inline = False
            )

            for txtchnls in list(selected_lobby.user_channels.keys()):
                on_tie_msg: discord.TextChannel = await txtchnls.send(embed = on_tie)
                selected_lobby.current_messages.append(on_tie_msg)

            for d_plrs in selected_lobby.lobby_game.players:
                d_plrs.invoke_graveyard()
                d_plrs.invoke_hand()

        # wait              
        await asyncio.sleep(3)

        # clearing out and reorganizing winnigs
        for new_msgs in selected_lobby.current_messages: await new_msgs.delete()
        selected_lobby.current_messages.clear()

        # checking for match winner (end game)
        winning_match_player: player = selected_lobby.lobby_game.check_match_condition()
        winning_match_user: discord.Member

        for usr, plr in selected_lobby.get().get('user_players').items():
            if winning_match_player == plr: winning_match_user = usr

        if (winning_match_player):
            # end game and clean up stuff
            on_game_end: discord.Embed = discord.Embed(
                title = 'end of the game',
                description = f'{winning_match_user.mention} has won',
                color = 0xDDDDDD
            )

            crd_string: str = (f'')
            for new_crd in selected_lobby.lobby_game.won_cards.get(winning_match_player):
                type: str = CARD_CONVERSIONS.get(new_crd.get().get('type'))
                color: str = CARD_CONVERSIONS.get(new_crd.get().get('color'))
                rank: str = CARD_CONVERSIONS.get(new_crd.get().get('rank'))

                new_str: str = f'''{type} {color} {rank}◾◾'''
                crd_string += new_str

            on_game_end.add_field(
                name = 'winners winning cards',
                value = f'{crd_string}',
                inline = False
            )

            on_bye_end: discord.Embed = discord.Embed(
                title = 'the lobby will close momentarily',
                color = 0xDDDDDD
            )

            for txtchnls in list(selected_lobby.user_channels.keys()):
                on_end_msg: discord.TextChannel = await txtchnls.send(embed = on_game_end)
                on_bye_msg: discord.TextChannel = await txtchnls.send(embed = on_bye_end)

            await asyncio.sleep(5)
            await clear_lobby(selected_lobby)

            return

        await display_options(selected_lobby)

    elif (lobby_players[0].selected_card != None and lobby_players[1].selected_card != None):
        for msgs in selected_lobby.current_messages: await msgs.delete()
        selected_lobby.current_messages.clear()

        # checking for round winner
        winning_round_player: player = selected_lobby.lobby_game.check_round_condition()
        winning_round_user: discord.Member

        for usr, plr in selected_lobby.get().get('user_players').items():
            if winning_round_player == plr: winning_round_user = usr

        if (winning_round_player):
            losing_round_player: player 
            for plrs in selected_lobby.lobby_game.players:
                if plrs != winning_round_player: losing_round_player = plrs

            w_type: str = CARD_CONVERSIONS.get(winning_round_player.selected_card.get().get('type'))
            w_color: str = CARD_CONVERSIONS.get(winning_round_player.selected_card.get().get('color'))
            w_rank: str = CARD_CONVERSIONS.get(winning_round_player.selected_card.get().get('rank'))

            l_type: str = CARD_CONVERSIONS.get(losing_round_player.selected_card.get().get('type'))
            l_color: str = CARD_CONVERSIONS.get(losing_round_player.selected_card.get().get('color'))
            l_rank: str = CARD_CONVERSIONS.get(losing_round_player.selected_card.get().get('rank'))

            on_winning_player: discord.Embed = discord.Embed(
                title = 'results',
                description = f'{winning_round_user.mention} won the round',
                color = 0xDDDDDD
            )
            
            on_winning_player.add_field(
                name = 'chosen cards',
                value = f'''{w_type} {w_color} {w_rank}◾vs◾{l_type} {l_color} {l_rank}''',
                inline = False
            )

            for txtchnls in list(selected_lobby.user_channels.keys()):
                round_winning_msg: discord.TextChannel = await txtchnls.send(embed = on_winning_player)
                selected_lobby.current_messages.append(round_winning_msg)

            # updating values
            selected_lobby.lobby_game.won_cards.get(winning_round_player).append(winning_round_player.selected_card)

            for d_plrs in selected_lobby.lobby_game.players:
                d_plrs.invoke_graveyard()
                d_plrs.invoke_hand()

        elif (winning_round_player is None):
            a_type: str = CARD_CONVERSIONS.get(selected_lobby.lobby_game.players[0].selected_card.get().get('type'))
            a_color: str = CARD_CONVERSIONS.get(selected_lobby.lobby_game.players[0].selected_card.get().get('color'))
            a_rank: str = CARD_CONVERSIONS.get(selected_lobby.lobby_game.players[0].selected_card.get().get('rank'))

            b_type: str = CARD_CONVERSIONS.get(selected_lobby.lobby_game.players[1].selected_card.get().get('type'))
            b_color: str = CARD_CONVERSIONS.get(selected_lobby.lobby_game.players[1].selected_card.get().get('color'))
            b_rank: str = CARD_CONVERSIONS.get(selected_lobby.lobby_game.players[1].selected_card.get().get('rank'))


            on_tie: discord.Embed = discord.Embed(
                title = 'results',
                description = f'neither player won the round',
                color = 0xDDDDDD
            )

            on_tie.add_field(
                name = 'chosen cards',
                value = f'''{a_type} {a_color} {a_rank}◾vs◾{b_type} {b_color} {b_rank}''',
                inline = False
            )

            for txtchnls in list(selected_lobby.user_channels.keys()):
                on_tie_msg: discord.TextChannel = await txtchnls.send(embed = on_tie)
                selected_lobby.current_messages.append(on_tie_msg)

            for d_plrs in selected_lobby.lobby_game.players:
                d_plrs.invoke_graveyard()
                d_plrs.invoke_hand()

        # wait              
        await asyncio.sleep(3)

        # clearing out and reorganizing winnigs
        for new_msgs in selected_lobby.current_messages: await new_msgs.delete()
        selected_lobby.current_messages.clear()

        # checking for match winner (end game)
        winning_match_player: player = selected_lobby.lobby_game.check_match_condition()
        winning_match_user: discord.Member

        for usr, plr in selected_lobby.get().get('user_players').items():
            if winning_match_player == plr: winning_match_user = usr

        if (winning_match_player):
            # end game and clean up stuff
            on_game_end: discord.Embed = discord.Embed(
                title = 'end of the game',
                description = f'{winning_match_user.mention} has won',
                color = 0xDDDDDD
            )

            crd_string: str = (f'')
            for new_crd in selected_lobby.lobby_game.won_cards.get(winning_match_player):
                type: str = CARD_CONVERSIONS.get(new_crd.get().get('type'))
                color: str = CARD_CONVERSIONS.get(new_crd.get().get('color'))
                rank: str = CARD_CONVERSIONS.get(new_crd.get().get('rank'))

                new_str: str = f'''{type} {color} {rank}◾'''
                crd_string += new_str

            on_game_end.add_field(
                name = 'winners winning cards',
                value = f'{crd_string}',
                inline = False
            )

            on_bye_end: discord.Embed = discord.Embed(
                title = 'the lobby will close momentarily',
                color = 0xDDDDDD
            )

            for txtchnls in list(selected_lobby.user_channels.keys()):
                on_end_msg: discord.TextChannel = await txtchnls.send(embed = on_game_end)
                on_bye_msg: discord.TextChannel = await txtchnls.send(embed = on_bye_end)

            await asyncio.sleep(5)
            await clear_lobby(selected_lobby)

            return

        await display_options(selected_lobby)

# dead functions
async def on_option_pick_one(
        bot: discord.Client, 
        msg: discord.Message,
        us: discord.User,
        **kwargs) -> None:
    await on_option_pick(bot, msg, us, 0, **kwargs)

async def on_option_pick_two(
        bot: discord.Client, 
        msg: discord.Message,
        us: discord.User,
        **kwargs) -> None:
    await on_option_pick(bot, msg, us, 1, **kwargs)

async def on_option_pick_three(
        bot: discord.Client, 
        msg: discord.Message,
        us: discord.User,
        **kwargs) -> None:
    await on_option_pick(bot, msg, us, 2, **kwargs)