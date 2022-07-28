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
    record_id = message.content.replace('/ud-get ','')
    return ud_battle.discord_battle(message, storage.get_battle(record_id))
