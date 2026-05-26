#!/bin/bash

# Start web server in background
gunicorn app:app --bind 0.0.0.0:$PORT &

# Start Telegram bot
python bot.py
