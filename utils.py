import asyncio
import logging
import aiohttp
import traceback
import random
import string
import base64
import time as t
from datetime import datetime, timedelta, date, time
import pytz

from database.users_db import db
from Script import script
from info import *

# -------------------------- LOGGER -------------------------- #
logger = logging.getLogger(__name__)

# -------------------------- TEMP STORAGE -------------------------- #
class temp:
    ME = None
    BOT = None
    U_NAME = None
    B_NAME = None
    TOKENS = {}
    VERIFIED = {}

# -------------------------- PING SERVER -------------------------- #
async def ping_server():
    while True:
        await asyncio.sleep(PING_INTERVAL)
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10)
            ) as session:
                async with session.get(URL) as resp:
                    logger.info(f"✅ Pinged server: {resp.status}")
        except Exception as e:
            logger.error(f"❌ Ping error: {e}")
            traceback.print_exc()

# -------------------------- FILE SIZE -------------------------- #
def get_size(size: int) -> str:
    units = ["Bytes", "KB", "MB", "GB", "TB"]
    size = float(size)
    i = 0
    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1
    return f"{size:.2f} {units[i]}"

# -------------------------- READABLE TIME -------------------------- #
def get_readable_time(seconds: int) -> str:
    result = []
    for unit in ("s", "m", "h", "d"):
        seconds, rem = divmod(seconds, 60 if unit != "d" else 24)
        if rem:
            result.append(f"{int(rem)}{unit}")
    return " ".join(reversed(result)) if result else "0s"

# -------------------------- NORMAL SHORT LINK -------------------------- #
async def get_shortlink(link):
    API = SHORTLINK_API
    URL = SHORTLINK_URL

    if not link.startswith("https"):
        link = link.replace("http", "https", 1)

    if URL == "api.shareus.in":
        url = f"https://{URL}/shortLink"
        params = {"token": API, "format": "json", "link": link}
    else:
        url = f"https://{URL}/api"
        params = {"api": API, "url": link}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, ssl=False) as response:
                data = await response.json(content_type=None)
                if data.get("status") == "success":
                    return data.get("shortlink") or data.get("shortenedUrl")
    except Exception as e:
        logger.error(f"Shorten error: {e}")

    return link

# -------------------------- ENCRYPT VERIFY LINK -------------------------- #
def encrypt_verify_link(url: str, user_id: int, expiry=600) -> str:
    expire_at = int(t.time()) + expiry
    raw = f"{url}|{user_id}|{expire_at}|{VERCEL_SECRET_KEY}"
    return base64.urlsafe_b64encode(raw.encode()).decode()

# -------------------------- TOKEN CHECK -------------------------- #
async def check_token(bot, userid, token):
    user = await bot.get_users(userid)
    tokens = temp.TOKENS.get(user.id, {})
    return tokens.get(token) is False

# -------------------------- TOKEN GENERATOR (UPDATED) -------------------------- #
async def get_token(bot, userid, link=None):
    user = await bot.get_users(userid)

    # Generate token
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    temp.TOKENS[user.id] = {token: False}

    # 🔥 FINAL BOT VERIFY LINK (AFTER SHORTENER)
    bot_verify_link = f"https://t.me/{BOT_USERNAME}?start=verify-{user.id}-{token}"

    # Encrypt BOT link (NOT shortener, NOT direct)
    encrypted = encrypt_verify_link(
        bot_verify_link,
        user.id,
        expiry=VERIFY_EXPIRE
    )

    # Vercel will open → shortener → bot
    return f"{VERCEL_VERIFY_URL}?d={encrypted}"

# -------------------------- GET VERIFY STATUS -------------------------- #
async def get_verify_status(userid):
    status = temp.VERIFIED.get(userid)
    if not status:
        status = await db.get_verified(userid)
        temp.VERIFIED[userid] = status
    return status

# -------------------------- UPDATE VERIFY STATUS -------------------------- #
async def update_verify_status(userid, date_temp, time_temp):
    status = await get_verify_status(userid)
    status["date"] = date_temp
    status["time"] = time_temp
    temp.VERIFIED[userid] = status
    await db.update_verification(userid, date_temp, time_temp)

# -------------------------- VERIFY USER -------------------------- #
async def verify_user(bot, userid, token):
    user = await bot.get_users(int(userid))
    temp.TOKENS[user.id] = {token: True}

    tz = pytz.timezone("Asia/Kolkata")
    expiry = datetime.now(tz) + timedelta(seconds=VERIFY_EXPIRE)

    await update_verify_status(
        user.id,
        expiry.strftime("%Y-%m-%d"),
        expiry.strftime("%H:%M:%S")
    )

# -------------------------- CHECK VERIFICATION -------------------------- #
async def check_verification(bot, userid):
    user = await bot.get_users(int(userid))
    tz = pytz.timezone("Asia/Kolkata")

    now = datetime.now(tz)
    status = await get_verify_status(user.id)

    if not status:
        return False

    try:
        exp_date = datetime.strptime(status["date"], "%Y-%m-%d").date()
        exp_time = datetime.strptime(status["time"], "%H:%M:%S").time()
    except Exception as e:
        logger.error(f"Verification parse error: {e}")
        return False

    if exp_date < now.date():
        return False
    if exp_date == now.date() and exp_time < now.time():
        return False

    return True
