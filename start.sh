#!/bin/bash

echo "Starting web server (gunicorn)..."
gunicorn app:app --bind 0.0.0.0:$PORT &

echo "Starting Telegram bot..."
python bot.py
