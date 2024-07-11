import logging
import subprocess
import datetime
import asyncio
import os
import requests
import time
from p_bar import progress_bar
import aiohttp
import tgcrypto
import aiofiles
import speedtest
from pyrogram.types import Message
from pyrogram import Client, filters
from config import log_channel

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def run_speedtest(m):
    """
    Run a speed test and return the results.
    """
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit_text("<b>⇆ Running download speed test...</b>")
        test.download()
        m = m.edit_text("<b>⇆ Running upload speed test...</b>")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit_text("<b>↻ Sharing speed test results...</b>")
    except Exception as e:
        return m.edit_text(str(e))
    return result


def get_video_duration(filename):
    """
    Get the duration of a video file.
    """
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
        "default=noprint_wrappers=1:nokey=1", filename
    ],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return float(result.stdout)


async def download_file(url, name):
    """
    Download a file from a URL and save it with the specified name.
    """
    file_path = f'{name}.pdf'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(file_path, mode='wb') as f:
                    await f.write(await resp.read())
    return file_path


async def download_file_with_cookies(url, name, cookies):
    """
    Download a file from a URL with cookies and save it with the specified name.
    """
    file_path = f'{name}.pdf'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, cookies=cookies) as resp:
            if resp.status == 200:
                async with aiofiles.open(file_path, mode='wb') as f:
                    await f.write(await resp.read())
    return file_path


async def run_command(cmd):
    """
    Run a shell command asynchronously and return the output.
    """
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    logging.info(f'[{cmd!r} exited with {proc.returncode}]')
    if proc.returncode != 0:
        return False
    if stdout:
        return stdout.decode()
    if stderr:
        return stderr.decode()


def download_file_old(url, file_name, chunk_size=1024 * 10):
    """
    Download a file from a URL using requests and save it with the specified name.
    """
    if os.path.exists(file_name):
        os.remove(file_name)
    r = requests.get(url, allow_redirects=True, stream=True)
    with open(file_name, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                fd.write(chunk)
    return file_name


def format_size(size, decimal_places=2):
    """
    Format a file size in human-readable form.
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def generate_filename():
    """
    Generate a unique filename based on the current date and time.
    """
    date = datetime.date.today()
    now = datetime.datetime.now()
    current_time = now.strftime("%H%M%S")
    return f"{date} {current_time}.mp4"


async def download_video_file(url, cmd, name):
    """
    Download a video file using a specified command and return the file name.
    """
    download_cmd = f'{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args "aria2c: -x 16 -j 32 --split=16 --max-connection-per-server=4"'
    global failed_counter
    logging.info(download_cmd)
    result = subprocess.run(download_cmd, shell=True)
    if "visionias" in cmd and result.returncode != 0 and failed_counter <= 10:
        failed_counter += 1
        await asyncio.sleep(5)
        await download_video_file(url, cmd, name)
    failed_counter = 0
    try:
        if os.path.isfile(name):
            return name
        elif os.path.isfile(f"{name}.webm"):
            return f"{name}.webm"
        name = name.split(".")[0]
        if os.path.isfile(f"{name}.mkv"):
            return f"{name}.mkv"
        elif os.path.isfile(f"{name}.mp4"):
            return f"{name}.mp4"
        elif os.path.isfile(f"{name}.mp4.webm"):
            return f"{name}.mp4.webm"
        return name
    except FileNotFoundError:
        return os.path.splitext(name)[0] + ".mp4"


async def send_video(bot: Client, m: Message, caption, filename, thumb, name, chat: int):
    """
    Send a video file to a Telegram chat.
    """
    subprocess.run(
        f'ffmpeg -i "{filename}" -ss 00:01:00 -vframes 1 "{filename}.jpg"',
        shell=True
    )

    try:
        thumbnail = thumb if thumb != "no" else f"{filename}.jpg"
    except Exception as e:
        await m.reply_text(str(e))

    dur = int(get_video_duration(filename))

    start_time = time.time()

    try:
        await bot.send_video(chat_id=chat, video=filename, caption=caption, supports_streaming=True, height=720, width=1280, thumb=thumbnail, duration=dur)
    except TimeoutError:
        await asyncio.sleep(5)
        await bot.send_video(chat_id=chat, video=filename, caption=caption, supports_streaming=True, height=720, width=1280, thumb=thumbnail, duration=dur)
    except Exception:
        await bot.send_video(chat_id=chat, video=filename, caption=caption, supports_streaming=True, height=720, width=1280, thumb=thumbnail, duration=dur)

    os.remove(filename)
    os.remove(f"{filename}.jpg")
