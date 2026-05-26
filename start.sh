#!/bin/bash

# Start web server with gunicorn
gunicorn app:app --bind 0.0.0.0:$PORT

