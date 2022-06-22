import battle_parser
import discord
import image_to_text
import json
import hashlib
import re

def process(message):

    re_image_url = re.search("(?P<url>https?://[^\s]+)",  message.content)

    if re_image_url is not None:
        image_url = re_image_url.group("url")
    elif len(message.attachments) > 0:
        image_url = message.attachments[0].url
    else:
        return message.author.mention + ", did you forget the attachement?"

    texts = image_to_text.detect_text_uri(image_url)
    result = battle_parser.parse_text(texts, image_url)

    response_text = message.author.mention+", thanks for your contribution !\n"
    response_text = response_text + '```\n'
    response_text = response_text + json.dumps(result, indent=4, sort_keys=True)
    response_text = response_text + '```\n'

    return response_text
