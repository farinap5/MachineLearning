import os
import discord
import requests
import utils
import logging
import json
import cv2
import numpy as np
import tensorflow as tf

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)
# config log
logFile = "logs.txt"
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename=logFile)

# Temos um arquivo json contendo quais servers e canais o bot deve interagir com.
# O json deve ter listas como wrap do valor.
access = open("./access.json", "r").read()
accessDict = json.loads(access)

# TODO: Mover para utils
imgTypes = ["png","jpg","jpeg"]
imgFold = "./img/"


# Carregar modelo
model = tf.keras.saving.load_model("/root/test-v1.h5")

@client.event
async def on_ready():
    logging.info('{0.user} is up!'.format(client))
 
@client.event
async def on_message(message):
    #print(str(message.guild.id)+":",str(message.channel.id))
    # validar acesso com accessDict do access.json
    # É preciso melhorar isso, e tirar o "try except"
    try:
        if str(message.channel.id) not in accessDict[str(message.guild.id)]:
            return
    except :
        pass
    if message.author == client.user:
        return
    
    cmds = message.content.split(" ")
    if cmds[0] != "d":
        return


    ## --help
    if "--help" in message.content or "-h" in message.content:
        logging.info("Help asked from "+str(message.author))
        await message.channel.send(utils._help())
        return


    ## --image
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
            with open(imgFold+file_name, "wb") as f:
                f.write(attachURL.content)
                logging.info("File "+file_name+" written to disk from "+str(message.author))
                f.close
                #await message.channel.send("Imagem "+file_name+" salva.")

                image_size = (90, 90)
                imagem = cv2.imread(imgFold+file_name)
                imagem = cv2.resize(imagem, image_size)
                imagem = imagem.reshape((1,90,90,3))
                imagem = tf.cast(imagem/255. ,tf.float32)
                result_clss = model.predict(imagem)
                i = np.argmax(result_clss)
                classes = ["uma Margarida", "um Dente de leao", "uma Rosa", "um Girassol", "uma Tupila"]
                await message.channel.send("Esta imagem corresponde à " + classes[i])
                logging.info("Image "+file_name+" predicted.")





    ## --debug
    if "--debug" in message.content or "-d" in message.content:
        if len(cmds) == 3:
            if "access" == cmds[2]:
                await message.channel.send(str(accessDict))
        else:
            logging.info("User is debugging "+str(message.author))
            file = open(logFile, "r").readlines()
            await message.channel.send(f"""
```
{"".join(file[-20:-1])}        
```
""")
        return

client.run(os.getenv("DOSKYBOT"))
