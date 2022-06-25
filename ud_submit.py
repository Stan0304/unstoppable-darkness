import battle_parser
import discord
import emojis
import image_to_text
import json
import hashlib
import re


def process(message, client):

    re_image_url = re.search("(?P<url>https?://[^\s]+)",  message.content)

    if re_image_url is not None:
        image_url = re_image_url.group("url")
    elif len(message.attachments) > 0:
        image_url = message.attachments[0].url
    else:
        return "Did you forget the attachement?"

    texts = image_to_text.detect_text_uri(image_url)
    result = battle_parser.parse_text(texts, image_url)

    if 'message' in result.keys():
        return result['message']
    
    response_text = '\n'
    response_text = response_text + 'RecordId: 1' + '\n'
    response_text = response_text + 'Hash: ' + result['_unik'] + '\n'
    response_text = response_text + show_team(result, 'offensive_team', client) + '\n'
    response_text = response_text + show_team(result, 'deffensive_team', client) + '\n'
    response_text = response_text + '\n\n'
    response_text = response_text + result['_image_url'] + '\n'

    return response_text

def show_team(result, team, client):
    if team == 'offensive_team':
        text = 'Offensive Team ('
    elif team == 'deffensive_team':
        text = 'Deffensive Team ('
    
    text = text + str(result[team]['power'])
    text = text + 'k): '
    text = text + get_heroes(result, team, client)
    return text

def get_heroes(result, team, client):
    heroes_text = ""
    for hero_name in battle_parser.heroes_position:
        for hero in result[team]['heroes']:
            if hero['name'] == hero_name:
                heroes_text = heroes_text + emojis.get_hero_emoji(hero_name)
                power = int(hero['power'])
                heroes_text = heroes_text + ' (' + f'{power:,}' + '), '
    return heroes_text
