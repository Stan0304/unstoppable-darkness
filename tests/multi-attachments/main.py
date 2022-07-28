import re

content = "/ud https://media.discordapp.net/attachments/795675024593125406/930837291709128854/IMG_0151.png?width=1343&height=621 \
    https://media.discordapp.net/attachments/988510802506022975/989205361577820190/image.png?width=1345&height=621 \
    https://cdn.discordapp.com/attachments/988510802506022975/989190078205157506/unknown.png"

re_image_urls = re.findall("(?P<url>https?://[^\s]+)",  content)

for re_image_url in re_image_urls:
    print(re_image_url)
