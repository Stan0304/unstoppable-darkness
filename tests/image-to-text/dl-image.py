import requests
import shutil

r = requests.get('https://cdn.discordapp.com/attachments/988510802506022975/989190078205157506/unknown.png', stream=True)
if r.status_code == 200:
    with open("img.png", 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)