import os
import discord
import requests
import utils
import logging

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)
# config log
logFile = "logs.txt"
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename=logFile)


# TODO: Mover para utils
imgTypes = ["png","jpg","jpeg"]
imgFold = "./img/"

@client.event
async def on_ready():
    logging.info('{0.user} is up!'.format(client))
 
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    cmds = message.content.split(" ")

    if cmds[0] != "d":
        return
    if "--help" in message.content or "-h" in message.content:
        logging.info("Help asked from "+str(message.author))
        await message.channel.send(utils._help())
        return
    if "--image" in message.content or "-i" in message.content:
        logging.info("Image pattern received from "+str(message.author))
        if message.attachments == []:
            logging.info("No attachments from "+str(message.author))
            await message.channel.send("No valid image!")
            return
        for attach in message.attachments:
            # Valida se a estensão do arquivo está na whitelist de extensões (i.e. png, jpg)
            if attach.url.split(".")[-1] not in imgTypes:
                logging.info("File type error from "+str(message.author))
                await message.channel.send("No valid image!")
                return
            
            # TODO: Criar função aleatória para o nome do arquivo. É ruim guardar arquivo com
            # o nome do attachment original, podemos ter conflotos.
            attachURL = requests.get(attach.url)
            file_name = attach.url.split('/')[-1]
            with open(imgFold+"/"+file_name, "wb") as f:
                f.write(attachURL.content)
                logging.info("File "+file_name+" written to disk from "+str(message.author))
                f.close
                await message.channel.send("Imagem "+file_name+" salva.")
    if "--debug" in message.content or "-d" in message.content:
        logging.info("User is debugging "+str(message.author))
        file = open(logFile, "r").readlines()
        await message.channel.send(f"""
```
{"".join(file[-20:-1])}        
```
""")
        return

client.run(os.getenv("DOSKYBOT"))
