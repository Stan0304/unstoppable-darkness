import hashlib
import image_to_text

texts = image_to_text.detect_text_uri('https://cdn.discordapp.com/attachments/795675024593125406/960445893113442364/IMG_5040.png')

print(texts)
print('--')

hash_object = hashlib.sha256(str(texts).encode('utf-8'))
print(hash_object.hexdigest())