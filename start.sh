#!/bin/bash

# Start the web server (Flask) in background
gunicorn app:app --bind 0.0.0.0:$PORT &

# Start the Telegram bot
python bot.py
