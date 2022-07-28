import battle_parser2
import discord
import emojis
import image_to_text
import json
import hashlib
import re
import storage
import ud_battle


def process(message, client):

    q_ids = []
    ids = re.findall("ids=[\w,]+",  message.content)
    for f_ids in ids:
        for id in f_ids[4:].split(','):
            q_ids.append(id)
    
    q_player = ""
    player = re.findall("player=[\w]+",  message.content)
    if len(player) > 0:
        q_player = player[0][7:]
    
    q_heroes = []
    heroes = re.findall("heroes=[\w,]+",  message.content)
    for f_hero in heroes:
        for hero in f_hero[7:].split(','):
            q_heroes.append(hero)

    
    return ud_battle.discord_battle(message, storage.query(q_ids, q_player, hero_index(q_heroes)))


def hero_index(q_heroes):
    index = ""
    for hero_pos in battle_parser2.heroes_position:
        for hero in q_heroes:
            if hero == hero_pos:
                hero_index = hero_pos
                index = index + '.*;' + hero_pos + ';'
    return index + '.*'