import re

message = "/ud https://media.discordapp.net/attachments/988510802506022975/989140339384258620/unknown.png"

re_image_url = re.search("(?P<url>https?://[^\s]+)", message)

if re_image_url is not None:
    image_url = re_image_url.group("url")
else:
    image_url = ""
    print("XXX, did you forget the attachement?")

print(image_url)