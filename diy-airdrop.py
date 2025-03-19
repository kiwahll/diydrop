import discord, os, re, base64
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image
from io import BytesIO

client = discord.Client(intents=discord.Intents.all())

TOKEN = "MTAyMTQyNTMzMzA0MTM4NTU4NA.G6HLGs.WTeNCvYiZqu0L0W2sSZhznbix5Jg8in0ldqfmo"
CHANNEL_ID = 1296174952487190590
# https://discord.com/api/webhooks/1296174978424901725/ofv1vgDM78shZKLKFZA97pe6S2PJ2qpzfbg37wQ_6rZTA_BVi6UQyAliaHh5BSo35bV5
url_regex = re.compile(r"^(http|https)://")
icon_img_base64 = b"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"

def on_exit_clicked(icon, item):
    os._exit(0)

icon('DIY Airdrop', Image.open(BytesIO(base64.b64decode(icon_img_base64))), menu=menu(
    item(
        'Stop',
        on_exit_clicked))).run_detached()


@client.event
async def on_ready():
    channel = client.get_channel(CHANNEL_ID)
    history = [x async for x in channel.history()]
    for item in history:
        message = item.content

        if url_regex.match(message):
            title_search = re.search(r"^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)", message, re.IGNORECASE)
            if title_search:
                title = title_search.group(1)
            else:
                title = history.index(item)

            with open(fr"C:\Users\{os.getlogin()}\Desktop\{title}.url", "w") as file:
                file.writelines(["[InternetShortcut]", "\n", "URL=" + message])
        elif message.startswith("image:"):
            img_data = b"" + message
            with open(fr"C:\Users\{os.getlogin()}\Desktop\{history.index(item)}.png", "w") as file:
                file.write(base64.decodebytes(img_data))
        else:
            with open(fr"C:\Users\{os.getlogin()}\Desktop\{history.index(item)}.txt", "w") as file:
                file.write(message)

    await channel.purge()

@client.event
async def on_message(message):
    if message.channel.id == CHANNEL_ID:
        history = [x async for x in message.channel.history()]
        for item in history:
            message = item.content

        if url_regex.match(message):
            title_search = re.search(r"^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)", message, re.IGNORECASE)
            if title_search:
                title = title_search.group(1)
            else:
                title = history.index(item)

            with open(fr"C:\Users\{os.getlogin()}\Desktop\{title}.url", "w") as file:
                file.writelines(["[InternetShortcut]", "\n", "URL=" + message])
        elif message.startswith("image:"):
            img_data = b"" + message
            with open(fr"C:\Users\{os.getlogin()}\Desktop\{history.index(item)}.png", "w") as file:
                file.write(base64.decodebytes(img_data))
        else:
            with open(fr"C:\Users\{os.getlogin()}\Desktop\{history.index(item)}.txt", "w") as file:
                file.write(message)
        
        await client.get_channel(CHANNEL_ID).purge()

client.run(TOKEN)
