import hashlib
import image_to_text
import battle_parser2

#image_url = 'https://cdn.discordapp.com/attachments/988510802506022975/989190078205157506/unknown.png'
image_url = 'https://media.discordapp.net/attachments/795675024593125406/930837291709128854/IMG_0151.png?width=1343&height=621'
#image_url = 'https://media.discordapp.net/attachments/988510802506022975/989205361577820190/image.png?width=1345&height=621'
poster = 'stan'
texts = image_to_text.detect_text_uri(image_url)

print(str(texts))
print('--')

hash_object = hashlib.sha256(str(texts).encode('utf-8'))
print(hash_object.hexdigest())
print('--')

result = battle_parser2.parse_text(texts, image_url, poster)

print(result)