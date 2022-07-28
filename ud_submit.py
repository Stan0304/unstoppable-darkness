import battle_parser2
import discord
import emojis
import image_to_text
import json
import hashlib
import re
import ud_battle


def process(message, client):

    re_image_urls = re.findall("(?P<url>https?://[^\s]+)",  message.content)

    returns = []
    if len(re_image_urls) > 0:
        for re_image_url in re_image_urls:
            returns.append(process_battle(message, client, re_image_url))
    elif len(message.attachments) > 0:
        for attachment in message.attachments:
            returns.append(process_battle(message, client, attachment.url))
    
    if len(returns) > 0:
        return returns

    raise Exception('Did you forget the attachment')

def process_battle(message, client, image_url):

    texts = image_to_text.detect_text_uri(image_url)
    result = battle_parser2.parse_text(texts, image_url, message.author.display_name)

    return ud_battle.discord_battle(message, result)
