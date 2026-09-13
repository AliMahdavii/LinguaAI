import os

from dotenv import load_dotenv
import telebot

from services.translation import translate_text


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "Hi"
    )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text

    translated_text = translate_text(
        user_text,
        "Persian"
    )

    bot.reply_to(
        message,
        translate_text
    )


def main():
    print("LinguaAI is running...")
    bot.infinity_polling()


if __name__ == "__main__":
    main()
