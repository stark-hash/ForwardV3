import logging
import os
import psutil
import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.constants import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler, filters, CallbackContext

from pymongo import MongoClient
from config import BOT_TOKEN, MONGODB_URI

# Initialize logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Telegram bot
bot = telegram.Bot(token=BOT_TOKEN)

# Create a MongoDB client
mongo_client = MongoClient(MONGODB_URI)
db = mongo_client['Cluster0']  # Replace with your actual database name
user_settings_collection = db['user_settings']
forwarded_messages_collection = db['forwarded_messages']

# Define conversation states if needed
STATE_ONE, STATE_TWO = range(2)
CHOOSING, SELECT_OPTION, SETTING_NAME, SETTING_VALUE = range(4)

# Define command handlers
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_html(
        f"ʜɪ {user.mention_html()}!\n"
        f"ɪ'ᴍ ᴀ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀᴜᴛᴏ ꜰᴏʀᴡᴀʀᴅ ʙᴏᴛ\n"
        f"ɪ ᴄᴀɴ ꜰᴏʀᴡᴀʀᴅ ᴀʟʟ ᴍᴇssᴀɢᴇ ꜰʀᴏᴍ ᴏɴᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴀɴᴏᴛʜᴇʀ ᴄʜᴀɴɴᴇʟ\n"
        f"ᴄʟɪᴄᴋ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ᴍᴇ"
    )
    return ConversationHandler.END
    
def donate(update: Update, context: CallbackContext):
    donate_message = (
        "If you liked me ❤️, consider making a donation to support my developer 👦\n"
        "UPI ID - `krishna527062@oksbi`"
    )
    update.message.reply_text(donate_message, parse_mode=ParseMode.MARKDOWN)


def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🔆 HELP\n"
        "📚 Available commands:\n"
        "⏣ /start - check I'm alive\n"
        "⏣ /forward - forward messages\n"
        "⏣ /private_forward - forward messages from private chat\n"
        "⏣ /unequify - delete duplicate media messages in chats\n"
        "⏣ /settings - configure your settings\n"
        "⏣ /stop - stop your ongoing tasks\n"
        "⏣ /reset - reset your settings\n"
        "\n"
        "💢 Features:\n"
        "► Forward message from public channel to your channel without admin permission. if the channel is private need admin permission\n"
        "► Forward message from private channel to your channel by using userbot(user must be member in there)\n"
        "► custom caption\n"
        "► custom button\n"
        "► support restricted chats\n"
        "► skip duplicate messages\n"
        "► filter type of messages\n"
        "► skip messages based on extensions & keywords & size"
    )

def private_forward(update: Update, context: CallbackContext):
    # Handle private forwarding of messages
    pass

    
def forward_message(update: Update, context: CallbackContext):
    # Handle forwarding messages from one chat to another
    pass


# Dictionary to store user settings
user_settings = {}

# Function to start the settings conversation
def start_settings(update: Update, context: CallbackContext):
    user = update.effective_user
    reply_keyboard = [
        [InlineKeyboardButton("Bots", callback_data="bots"), InlineKeyboardButton("Channels", callback_data="channels")],
        [InlineKeyboardButton("Caption", callback_data="caption")],
        [InlineKeyboardButton("Database", callback_data="database"), InlineKeyboardButton("Filters", callback_data="filters")],
        [InlineKeyboardButton("Button", callback_data="button")],
        [InlineKeyboardButton("Back", callback_data="back")]
    ]

    update.message.reply_html(
        f"Hi {user.mention_html()}! Change your settings as you wish.",
        reply_markup=InlineKeyboardMarkup(reply_keyboard)
    )

    return CHOOSING

# Function to handle user choice in settings
def select_option(update: Update, context: CallbackContext):
    query = update.callback_query
    option = query.data
    user_settings['current_option'] = option

    if option == 'bots':
        query.message.reply_html("You can manage your bots here.")
    elif option == 'channels':
        query.message.reply_html("Change your settings as your wish.")
    elif option == 'caption':
        query.message.reply_text("🖋️ Custom Caption\n\nYou can set a custom caption to videos and documents. Normally, you would use the default caption. Available fillings include:\n\n• {filename} : File Name\n• {size} : File Size\n• {caption} : original caption")
    elif option == 'database':
        query.message.reply_text("🗃️ Database\n\nA database is necessary to store your duplicate messages and for the de-duplication process.")
    elif option == 'filters':
        query.message.reply_text("🌟 Custom Filters\n\nConfigure the type of messages which you want to forward.")
    elif option == 'button':
        query.message.reply_text("🔘 Custom Button\n\nYou can add inline buttons to messages with the following format:\n\nSingle Button in a row:\n\n[forward bot][buttonurl:https://t.me/mdforwardbot]\n\nMore than one button in the same row:\n\n[forward bot][buttonurl:https://t.me/mdforwardbot]\n[forward bot][buttonurl:https://t.me/mdforwardbot(:same)]")
    elif option == 'back':
        return end_settings(update, context)

    return CHOOSING

# Function to end the settings conversation
def end_settings(update: Update, context: CallbackContext):
    query = update.callback_query
    query.message.reply_text("Your settings have been updated.")
    query.message.reply_text("Change your settings as your wish.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def how_to_use(update: Update, context: CallbackContext):
    update.message.reply_text(
        "⚠️ Before Forwarding:\n"
        "► First add a bot or userbot\n"
        "► Add at least one target channel (your bot/userbot must be admin there)\n"
        "► You can add chats or bots by using /settings\n"
        "► If the Source Channel is private, your userbot must be a member there, or your bot must need admin permission there also\n"
        "► Then use /forward to forward messages"
    )


def status(update: Update, context: CallbackContext):
    # Calculate statistics
    total_users = user_collection.count_documents({})
    total_bots = user_collection.count_documents({"is_bot": True})
    total_forwarded_messages = forwarded_messages_collection.count_documents({})
    
    # You should implement the logic to count unequified messages
    total_unequified_messages = 0  # Implement this
    
    status_message = (
        f"╔════❰ ʙᴏᴛ sᴛᴀᴛᴜs ❱═❍⊱❁۪۪\n"
        f"║╭━━━━━━━━━━━━━━━➣\n"
        f"║┣⪼👱 ᴛᴏᴛᴀʟ ᴜsᴇʀs: {total_users}\n"
        f"║┃\n"
        f"║┣⪼🤖 ᴛᴏᴛᴀʟ ʙᴏᴛ: {total_bots}\n"
        f"║┃\n"
        f"║┣⪼🔃 ғᴏʀᴡᴀʀᴅɪɴɢs: {total_forwarded_messages}\n"
        f"║┃\n"
        f"║┣⪼🔍 ᴜɴᴇǫᴜɪꜰʏɪɴɢs: {total_unequified_messages}\n"
        f"║╰━━━━━━━━━━━━━━━➣\n"
        f"╚══════════════════❍⊱❁۪۪"
    )
    
    update.message.reply_text(status_message, parse_mode='Markdown')

def server_status(update: Update, context: CallbackContext):
    # Get server status information
    total_disk_space = psutil.disk_usage('/').total / (1024 ** 3)  # Convert to GB
    used_disk_space = psutil.disk_usage('/').used / (1024 ** 3)  # Convert to GB
    free_disk_space = psutil.disk_usage('/').free / (1024 ** 3)  # Convert to GB
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent

    status_message = (
        f"╔════❰ sᴇʀᴠᴇʀ sᴛᴀᴛs ❱═❍⊱❁۪۪\n"
        f"║╭━━━━━━━━━━━━━━━➣\n"
        f"║┣⪼ ᴛᴏᴛᴀʟ ᴅɪsᴋ sᴘᴀᴄᴇ: {total_disk_space:.2f} GB\n"
        f"║┣⪼ ᴜsᴇᴅ: {used_disk_space:.2f} GB\n"
        f"║┣⪼ ꜰʀᴇᴇ: {free_disk_space:.2f} GB\n"
        f"║┣⪼ ᴄᴘᴜ: {cpu_usage}%\n"
        f"║┣⪼ ʀᴀᴍ: {ram_usage}%\n"
        f"║╰━━━━━━━━━━━━━━━➣\n"
        f"╚══════════════════❍⊱❁۪۪"
    )

    update.message.reply_text(status_message, parse_mode='Markdown')
    
def bots(update: Update, context: CallbackContext):
    # Handle bot management (add, remove, etc.)
    pass
    
def dummy_bot(update: Update, context: CallbackContext):
    # Handle adding a dummy bot
    pass
    
def user_bot(update: Update, context: CallbackContext):
    # Handle adding a userbot
    pass

def main():
    # Initialize the Updater and dispatcher
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

# Create the handlers
start_handler = CommandHandler('start', start)
donate_handler = CommandHandler('donate', donate)
help_handler = CommandHandler('help', help_command)
private_forward_handler = CommandHandler('private_forward', private_forward)
forward_message_handler = CommandHandler('forward', forward_message)
how_to_use_handler = CommandHandler('how_to_use', how_to_use)
status_handler = CommandHandler('status', status)
server_status_handler = CommandHandler('server_status', server_status)
bots_handler = CommandHandler('bots', bots)
dummy_bot_handler = CommandHandler('dummy_bot', dummy_bot)
user_bot_handler = CommandHandler('user_bot', user_bot)

# Add the handlers to the dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(donate_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(private_forward_handler)
dispatcher.add_handler(forward_message_handler)
dispatcher.add_handler(how_to_use_handler)
dispatcher.add_handler(status_handler)
dispatcher.add_handler(server_status_handler)
dispatcher.add_handler(bots_handler)
dispatcher.add_handler(dummy_bot_handler)
dispatcher.add_handler(user_bot_handler)

# Initialize the Updater and dispatcher
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Start the Bot
updater.start_polling()
updater.idle()


