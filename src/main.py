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


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text

    bot.reply_to(
        message,
        f"📝 متن دریافت شد:\n\n{user_text}"
    )


def main():
    print("LinguaAI is running...")
    bot.infinity_polling()


if __name__ == "__main__":
    main()
