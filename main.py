import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from yt_dlp import YoutubeDL

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
TOKEN = os.environ["TOKEN"]

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
pytgcalls = PyTgCalls(app)

ydl_opts = {'format': 'bestaudio', 'quiet': True}
ydl = YoutubeDL(ydl_opts)

@app.on_message(filters.command("play") & filters.group)
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply("اكتب /play اسم الأغنية")
    
    query = " ".join(message.command[1:])
    m = await message.reply(f"بدور على: {query}")
    
    info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
    url = info['url']
    title = info['title']
    
    await pytgcalls.join_group_call(
        message.chat.id,
        AudioPiped(url),
    )
    await m.edit(f"▶️ **شغال دلوقتي:** {title}")

@app.on_message(filters.command("stop") & filters.group)
async def stop(_, message):
    await pytgcalls.leave_group_call(message.chat.id)
    await message.reply("⏹️ وقفت")

pytgcalls.start()
app.run()
