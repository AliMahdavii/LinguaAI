import os

from dotenv import load_dotenv
import telebot

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "Hi"
    )


def main():
    print("LinguaAI is running...")
    bot.infinity_polling()


if __name__ == "__main__":
    main()
