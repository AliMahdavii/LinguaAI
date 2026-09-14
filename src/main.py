import os

import telebot
from telebot import types
from dotenv import load_dotenv

from src.services.translator_service import TranslatorService
from src.database import create_database, save_language, get_language


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set.")


bot = telebot.TeleBot(BOT_TOKEN)

translator = TranslatorService()


create_database()


LANGUAGES = {
    "Persian": "🇮🇷 Persian",
    "English": "🇬🇧 English",
    "German": "🇩🇪 German",
    "French": "🇫🇷 French",
    "Spanish": "🇪🇸 Spanish",
}


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    for language, label in LANGUAGES.items():
        keyboard.add(
            types.InlineKeyboardButton(
                label,
                callback_data=f"lang:{language}"
            )
        )

    bot.send_message(
        message.chat.id,
        "👋 Welcome to LinguaAI!\n\n"
        "Choose your target language:",
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("lang:"))
def select_language(call):
    language = call.data.split(":", 1)[1]

    save_language(
        call.from_user.id,
        language
    )

    bot.answer_callback_query(call.id)

    bot.send_message(
        call.message.chat.id,
        f"✅ Target language set to {language}.\n\n"
        "Now send me a text to translate."
    )



@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text

    target_language = get_language(
        message.from_user.id
    )

    if not target_language:
        bot.reply_to(
            message,
            "Please use /start first and choose a target language."
        )
        return

    try:
        result = translator.translate(
            user_text,
            target_language
        )

        response = (
            f"🌐 Source: {result.source_language}\n\n"
            f"🇮🇷 Translation:\n"
            f"{result.translation}"
        )

        if result.expression:
            response += (
                f"\n\n💡 Expression:\n"
                f'"{result.expression}"\n'
                f"{result.expression_meaning}"
            )

        bot.reply_to(
            message,
            response
        )

    except ValueError as error:
        print(f"Translation error: {error}")

        bot.reply_to(
            message,
            "⚠️ I couldn't process the translation correctly. "
            "Please try again."
        )

    except Exception as error:
        print(f"Unexpected error: {error}")

        bot.reply_to(
            message,
            "❌ Something went wrong. Please try again later."
        )


def main():
    print("LinguaAI is running...")
    bot.infinity_polling()


if __name__ == "__main__":
    main()
