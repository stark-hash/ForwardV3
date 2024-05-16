import os

# Pyrogram API credentials
API_ID = int(os.environ.get("API_ID", 18329555))
API_HASH = os.environ.get("API_HASH", "7bf83fddf8244fddfb270701e31470a8")

# Bot token
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7052097306:AAGtz7eZ1LFZzOJPOzSXtERURu7FEblX7wA")

# Pyrogram session name
SESSION_NAME = os.environ.get("SESSION_NAME")

# MongoDB URI (if you're using MongoDB)
MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb+srv://fdtekkz7:fadil777@cluster0.9euvogc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
