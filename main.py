import discord
import os
import traceback
import ud_submit


client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # Whitelist our server
    if message.guild.id != 988510802506022972:
        return

    # executes commands
    try:
        if message.content.startswith('/ud'):
            await message.channel.send(ud_submit.process(message))
    except Exception as e:
        traceback.print_exc()
        await message.channel.send(str(e))

client.run(os.getenv('TOKEN'))