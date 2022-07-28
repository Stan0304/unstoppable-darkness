import battle_parser2
import discord
import emojis

def discord_battle(message, result):
    embed=discord.Embed(
        title="Batlle processed", 
        description="RecordId: " + str(result['index']['record_id']) + "\nPostedBy: " + result['battle']['poster']  + \
            '\nPostedAt: ' + result['battle']['posted_at'], 
        color=discord.Color.blue())

    embed.set_image(url=result['battle']['image_url'])
    embed.set_thumbnail(url=message.author.avatar_url)

    embed.add_field(
        name="Offense team - " + str(result['battle']['offensive_team']['power']) + "k", 
        value='Result: ' + result['battle']['offensive_team']['result'] + '\n' + get_heroes(result, 'offensive_team') + '\n' + show_player(result, 'offensive_team'),
        inline=True)

    embed.add_field(
        name="Defensive team - " + str(result['battle']['defensive_team']['power']) + "k" ,
        value='Result: ' + result['battle']['defensive_team']['result'] + '\n' + get_heroes(result, 'defensive_team') + '\n' + show_player(result, 'defensive_team'),
        inline=True)
    embed.add_field(
        name="Did someone died within the offensive team ? " ,
        value='Run one of the following command to tell who died during the battle\n' + \
            '> ud-died ' + str(result['index']['record_id']) + ' ' + result['battle']['offensive_team']['heroes'][0]['name'] + '\n' + \
            '> ud-died ' + str(result['index']['record_id']) + ' ' + result['battle']['offensive_team']['heroes'][0]['name'] + ',' + result['battle']['offensive_team']['heroes'][1]['name'] + '\n' ,
        inline=False)

    return embed

def get_heroes(result, team):
    heroes_text = ""
    for hero_name in battle_parser2.heroes_position:
        for hero in result['battle'][team]['heroes']:
            if hero['name'] == hero_name:
                heroes_text = heroes_text + emojis.get_hero_emoji(hero_name)
                power = int(hero['power'])
                heroes_text = heroes_text + ' ' + f'{power:,}' + '\n'
    return heroes_text

def show_player(result, team):
    player_infos = []
    if 'player' in result['battle'][team]:
        player_infos.append('Player: '+result['battle'][team]['player'])
    if 'guild' in result['battle'][team]:
        player_infos.append('Guild: '+result['battle'][team]['guild'])
    if 'server' in result['battle'][team]:
        player_infos.append('Server: '+result['battle'][team]['guild'])

    return '\n'.join(x for x in player_infos)
