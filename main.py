from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
import requests
import json
import subprocess
from pyrogram import Client, filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyromod import listen
from pyrogram.types import Message
from p_bar import progress_bar
from subprocess import getstatusoutput
from aiohttp import ClientSession
import helper
from logger import logging
import time
import asyncio
from pyrogram.types import User, Message
from config import *
import sys
import re
import os
import config
from config import sudo_group, log_channel
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
import base64
import aiohttp
from datetime import datetime

batch = []

bot = Client(
    "LOVE",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    workers=8,
)

@bot.on_message(filters.command(["start"]) & filters.chat(sudo_group))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(f"Hello [{m.from_user.first_name}](tg://user?id={m.from_user.id}) \n use /txt to download txt\n")

@bot.on_message(filters.command("stop") & filters.chat(sudo_group))
async def restart_handler(_, m):
    await m.reply_text("**STOPPED**", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command("restart") & (filters.chat(sudo_group)))
async def restart_handler(_, m):
    await m.reply_text("**Restarted! बस करो Bro अब थक गया हु 🥹**", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["txt"]) & filters.chat(sudo_group))
async def txt_handler(bot: Client, m: Message):
    if batch:
        await m.reply("**Already Process Running**", quote=True)
        return

    batch.append(f'{m.from_user.id}')
    editable = await m.reply_text(f"**Hello <b> [{m.from_user.first_name}](tg://user?id={m.from_user.id}),"\
    "\n\n**I'm Txt Uploader Bot**"\
    "\n\nSend TXT file :-</b>**")
    input: Message = await bot.listen(editable.chat.id)
    
    if input.document:
        x = await input.download()
        file_name, ext = os.path.splitext(os.path.basename(x))
        credit = f"**Downloaded by :** [{m.from_user.first_name}](tg://user?id={m.from_user.id})"
        
        try:
            with open(x, "r") as f:
                content = f.read()
            content = content.split("\n")
            links = [i.split("://", 1) for i in content]
            os.remove(x)
        except:
            await m.reply_text("Invalid file input.🥲")
            os.remove(x)
            return
    else:
        content = input.text
        content = content.split("\n")
        links = [i.split("://", 1) for i in content]
   
    await editable.edit(f"**Total Links in File are :-** `{len(links)}`\n\n**Send index no. 1 or where you want to download**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Enter Batch Name or send d for grabbing from text filename.**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    b_name = file_name if raw_text0 == 'd' else raw_text0
    
    await editable.edit("**Enter Video Resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    resolution_map = {
        "144": "256x144",
        "240": "426x240",
        "360": "640x360",
        "480": "854x480",
        "720": "1280x720",
        "1080": "1920x1080"
    }
    res = resolution_map.get(raw_text2, "NA")

    await editable.edit("**Enter Your Name or send `de` for use default or skip**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    CR = credit if raw_text3 == 'de' else ('' if raw_text3 == 'skip' else f'Downloaded By: {raw_text3}')
      
    await editable.edit("Now send the **Thumb url**\nEg : ```https://telegra.ph/file/0633f8b6a6f110d34f044.jpg```\n\nor Send `no`")
    input6: Message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    thumb = raw_text6

    await editable.edit("**Send the chat id where You want to forward Video or Send** `de` **for default Channel**")
    input69: Message = await bot.listen(editable.chat.id)
    chat_id = input69.text
    await input69.delete(True)
    chat_id = -1002184158958 if chat_id == 'de' else chat_id

    await editable.delete()

    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb = "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)
        try:
            await bot.send_message(chat_id=int(chat_id), text=f"**𝐁𝐀𝐓𝐂𝐇 ➨ {b_name}**\n**TOTAL FILE ➨** **{len(links)}**")
            for i in range(count - 1, len(links)):
                V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
                url = "https://" + V

                if "visionias" in url:
                    async with ClientSession() as session:
                        async with session.get(url, headers={
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                            'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 
                            'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 
                            'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 
                            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Mobile Safari/537.36', 
                            'sec-ch-ua': '"Chromium";v="101", "Not=A?Brand";v="99"', 'sec-ch-ua-mobile': '?1', 
                            'sec-ch-ua-platform': '"Android"',
                        }) as resp:
                            text = await resp.text()
                            url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)
                
                elif "tencdn.classplusapp" in url or "media-cdn-alisg.classplusapp.com" in url or "videos.classplusapp" in url:
                    headers = {
                        'Host': 'api.classplusapp.com',
                        'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MTI0NzM1ODc2LCJvcmdJZCI6NDE4OTYxLCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTkwMjQ1NTQ1NzYiLCJuYW1lIjoiUmFodSIsImVtYWlsIjoicmFodWxjaG91aGFuMDc4MTVAZ21haWwuY29tIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJkZWZhdWx0TGFuZ3VhZ2UiOiJFTiIsImNvdW50cnlDb2RlIjoiSU4iLCJjb3VudHJ5SVNPIjoiOTEiLCJ0aW1lem9uZSI6IkdNVCs1OjMwIiwiaXNEaXkiOmZhbHNlLCJvcmdDb2RlIjoiZXV0cWQiLCJpc0RpeVN1YmFkbWluIjowLCJmaW5nZXJwcmludElkIjoiYjQwNDAxZTQ5MjFmM2IwZmFjMzM2OTQ3MDUxZTIiLCJpYXQiOjE3MjAzMzI4ODksImV4cCI6MTcyMDkzNzY4OX0.aMMH3B852Gu9Sof4AkXfHZsxgG0v53o00SNrzagnVpQgfsw_6b4ZHvqIFQ7dSBbU',
                        'user-agent': 'Mobile-Android', 
                        'app-version': '1.4.37.1', 
                        'api-version': '18', 
                        'device-id': '5d0d17ac8b3c9f51', 
                        'device-details': '2848b866799971ca_2848b8667a33216c_SDK-30', 
                        'accept-encoding': 'gzip'
                    }
                    params = (('url', f'{url}'),)
                    response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                    url = response.json()['url']
                
                elif '/master.mpd' in url:
                    id =  url.split("/")[-2]
                    url =  "https://penpencilvod.pc.cdn.bitgravity.com/" + id + "/master.m3u8"
                
                name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace(".", "").replace("'", "").replace('"', "").replace("%", "").replace("_", "").replace("-", "").replace("!", "").replace("(", "").replace(")", "").replace("]", "").replace("[", "").replace(",", "").replace("?", "").replace("~", "").replace("`", "").replace("...", "").replace("&", "").replace("♥️", "").strip()

                ytf = f"{name1[:50] if len(name1) > 50 else name1}[{i + 1}].mp4"

                if 'player.vimeo.com' in url:
                    try:
                        response = requests.get(url)
                        url = re.search(r'hls":\{"cdns"\:\{"akfire_interconnect_quic"\:.*?"url":"(.*?)","', response.text).group(1).replace("\\u0026", "&")
                    except Exception as e:
                        await bot.send_message(chat_id=log_channel, text=f"Error extracting Vimeo URL: {e}")

                if "visionias" in url or "classplusapp" in url:
                    try:
                        cmd = f'yt-dlp -o "{ytf}" --no-keep-video --no-warning --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0" "{url}"'
                        download_cmd = f"aria2c --file-allocation=none -c -x 16 -s 16 -k 1M '{url}' -o '{ytf}'"
                        file_path = f'{os.path.splitext(ytf)[0]}'
                        status, output = getstatusoutput(download_cmd)
                        if status != 0:
                            raise Exception(f"aria2c download failed with status {status}")
                        await helper.send_vid(bot, m, ytf, thumb, name1, CR, log_channel, res)
                    except Exception as e:
                        await bot.send_message(chat_id=log_channel, text=f"Error during downloading: {e}")
                else:
                    cmd = f'yt-dlp -o "{ytf}" --no-keep-video --no-warning --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0" "{url}"'
                    status, output = getstatusoutput(cmd)
                    if status != 0:
                        await bot.send_message(chat_id=log_channel, text=f"Error downloading video: {output}")
                    else:
                        await helper.send_vid(bot, m, ytf, thumb, name1, CR, log_channel, res)
        except Exception as e:
            await bot.send_message(chat_id=log_channel, text=f"**Video Downloading Error**\n\n```{e}```")
    batch.clear()

if __name__ == "__main__":
    bot.run()
