import discord
import os
import traceback
import ud_get
import ud_query
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
        if message.content.startswith('/ud-get'):
            response = ud_get.process(message, client)
            await message.reply(embed=response, mention_author=True)
        elif message.content.startswith('/ud-search'):
            response = ud_query.process(message, client)
            await message.reply(embed=response, mention_author=True)
        elif message.content.startswith('/ud'):
            responses = ud_submit.process(message, client)
            for response in responses:
                await message.reply(embed=response, mention_author=True)



#        if message.content.startswith('/emojis'):
#            str_emojis = ""
#            map_emojis = "server_emojis = {\n"
#            for emoji in client.emojis:
#                str_emojis = str_emojis + '<:' + emoji.name + ':' + str(emoji.id) + '> '
#                map_emojis = map_emojis + '\t"' + emoji.name + '": ' + '"<:' + emoji.name + ':' + str(emoji.id) + '>",\n'
#            
#            map_emojis = map_emojis + "}\n"
#            print(map_emojis)
#
#            await message.reply(str_emojis, mention_author=True)
#        
#        if message.content.startswith('/embed'):
#            embed=discord.Embed(title="Sample Embed", 
#                description="Embed box", 
#                color=discord.Color.red())

#            await message.reply(embed=embed, mention_author=True)
    except Exception:
        traceback.print_exc()
        error = traceback.format_exc()
        embed=discord.Embed(
            title="Error", 
            description="Sorry an error occured while processing your screenshot", 
            color=discord.Color.red())
        embed.add_field(
            name="Traceback (it should not be shared, only for testing purposes)", 
            value=error[:1024], 
            inline=False)
        await message.reply(embed=embed, mention_author=True)

client.run(os.getenv('TOKEN'))