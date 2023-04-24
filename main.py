import os
import discord
import requests
import utils

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

# TODO: Mover para utils
imgTypes = ["png","jpg","jpeg"]


@client.event
async def on_ready():
    print('{0.user} is up!'.format(client))
 
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    cmds = message.content.split(" ")

    if cmds[0] != "d":
        return
    if "--help" in message.content or "-h" in message.content:
        await message.channel.send(utils._help())
        return
    if "--image" in message.content or "-i" in message.content:
        if message.attachments == []:
            await message.channel.send("No valid image!")
            return
        for attach in message.attachments:
            # Valida se a estensão do arquivo está na whitelist de extensões (i.e. png, jpg)
            if attach.url.split(".")[-1] not in imgTypes:
                await message.channel.send("No valid image!")
                return
            
            # TODO: Criar função aleatória para o nome do arquivo. É ruim guardar arquivo com
            # o nome do attachment original, podemos ter conflotos.
            attachURL = requests.get(attach.url)
            file_name = attach.url.split('/')[-1]
            with open(file_name, "wb") as f:
                f.write(attachURL.content)
                f.close

client.run(os.getenv("DOSKYBOT"))
