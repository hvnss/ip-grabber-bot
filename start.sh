#!/bin/bash

# Start Flask web server in background
gunicorn app:app --bind 0.0.0.0:$PORT &

# Start Telegram bot in foreground
python bot.py
