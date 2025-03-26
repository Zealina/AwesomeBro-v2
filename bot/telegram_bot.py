"""Entry point"""

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import logging
from dotenv import load_dotenv


logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
)

# Load in environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError('BOT_TOKEN must be set')


# Command Handling
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Equator!")


app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler('start', start))


if __name__ == '__main__':
    app.run_polling()
