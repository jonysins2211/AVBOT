from pyrogram import Client, filters
from pyrogram.types import Message
from info import ADMINS
from database.users_db import db
from datetime import datetime

@Client.on_message(filters.private & filters.command("verified_users") & filters.user(ADMINS))
async def verified_users_list(client: Client, message: Message):
    # आज की तारीख (yyyy-mm-dd) के रूप में लो
    today = datetime.now().strftime("%Y-%m-%d")

    # केवल उन्हीं यूज़र्स को fetch करो जिनका verification आज हुआ है
    users = await db.users.find({
        "verification_status.date": today
    }).to_list(length=100)

    if not users:
        return await message.reply_text("❌ No users have been verified today")

    text = "✅ <b>Today Verified Users:</b>\n\n"
    for user in users:
        user_id = user.get("id")
        name = user.get("name", "Unknown")
        date = user.get("verification_status", {}).get("date", "❓")
        time = user.get("verification_status", {}).get("time", "❓")
        text += f"👤 <b>{name}</b> | <code>{user_id}</code>\n🗓️ {date} {time}\n\n"

    await message.reply_text(text)
