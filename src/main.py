import os

import telebot
from dotenv import load_dotenv

from src.services.translator_service import TranslatorService


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set.")


bot = telebot.TeleBot(BOT_TOKEN)
translator = TranslatorService()


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "👋 Welcome to LinguaAI!\n\n"
        "Send me a text and I'll translate it for you."
    )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text

    translated_text = translator.translate(
        user_text,
        "Persian"
    )

    bot.reply_to(
        message,
        translated_text
    )


def main():
    print("LinguaAI is running...")
    bot.infinity_polling()


if __name__ == "__main__":
    main()
