import json
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes
from parsing_cars import parsing_cars
import os
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('TOKEN_BOT')

async def start_bot(update:Update, context:ContextTypes.DEFAULT_TYPE)-> None:

    await update.message.reply_text("If you need help, write /help")

async def help_command(update:Update, context:ContextTypes.DEFAULT_TYPE)-> None:
    help_text = (
        "All commands: \n"
        "/start - Show command to get prices\n"
        "/get_prices - Get prices\n"
        "/help - Show this message\n"
    )
    await update.message.reply_text(help_text)



async def get_prices(update:Update, context:ContextTypes.DEFAULT_TYPE ) -> None:
    await update.message.reply_text("Please await 1-2 minutes...")

    parsing_cars()

    with open('prices.json', 'r', encoding='utf-8')as f:
        prices = json.load(f)

    message = (
        f" min_price : {prices['min_price']}\n"
        f" max_price : {prices['max_price']}\n"
        f" average_price: {prices['average_price']}\n"
    )

    await  update.message.reply_text(message)

def main() -> None:
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('get_prices', get_prices))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('start', start_bot))
    app.run_polling()

if __name__ == "__main__":
    main()
