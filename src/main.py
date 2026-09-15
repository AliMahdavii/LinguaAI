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

last_bot_messages = {}

user_messages = {}

create_database()


LANGUAGES = {
    "Persian": "🇮🇷 Persian",
    "English": "🇬🇧 English",
    "German": "🇩🇪 German",
    "French": "🇫🇷 French",
    "Spanish": "🇪🇸 Spanish",
}


def language_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    for language, label in LANGUAGES.items():
        keyboard.add(
            types.InlineKeyboardButton(
                label,
                callback_data=f"lang:{language}"
            )
        )

    return keyboard


def translation_keyboard():
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            "⚙️ Change Language",
            callback_data="change_language"
        )
    )

    return keyboard


@bot.message_handler(commands=["start"])
def start(message):

    chat_id = message.chat.id
    user_id = message.from_user.id

    # Delete previous messages
    previous_messages = user_messages.get(user_id, [])

    for message_id in previous_messages:
        try:
            bot.delete_message(
                chat_id,
                message_id
            )
        except Exception as error:
            print(f"Could not delete message: {error}")

    user_messages[user_id] = []

    target_language = get_language(user_id)

    if target_language:

        keyboard = types.InlineKeyboardMarkup()

        keyboard.add(
            types.InlineKeyboardButton(
                "⚙️ Change Language",
                callback_data="change_language"
            )
        )

        sent_message = bot.send_message(
            chat_id,
            f"👋 Welcome back to LinguaAI!\n\n"
            f"🌐 Target language: "
            f"{LANGUAGES[target_language]}\n\n"
            f"Send me a text to translate.",
            reply_markup=keyboard
        )

    else:

        sent_message = bot.send_message(
            chat_id,
            "👋 Welcome to LinguaAI!\n\n"
            "🌐 Choose your target language:",
            reply_markup=language_keyboard()
        )

    user_messages[user_id].append(
        sent_message.message_id
    )


@bot.callback_query_handler(
    func=lambda call: call.data == "change_language"
)
def change_language(call):
    bot.answer_callback_query(call.id)

    bot.edit_message_text(
        "🌐 Choose your target language:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=language_keyboard()
    )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("lang:")
)
def select_language(call):

    language = call.data.split(":", 1)[1]

    save_language(
        call.from_user.id,
        language
    )

    bot.answer_callback_query(
        call.id,
        "Language updated!"
    )

    bot.edit_message_text(
        f"✅ Target language: {LANGUAGES[language]}\n\n"
        "Send me a text to translate.",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=translation_keyboard()
    )


@bot.message_handler(func=lambda message: True)
def handle_message(message):

    user_id = message.from_user.id
    chat_id = message.chat.id
    user_text = message.text

    target_language = get_language(user_id)

    if not target_language:
        bot.reply_to(
            message,
            "Please use /start first and choose a target language."
        )
        return

    # Save user message ID
    user_messages.setdefault(user_id, []).append(
        message.message_id
    )

    # Show translating status
    translating_message = bot.send_message(
        chat_id,
        "⏳ Translating..."
    )

    try:

        result = translator.translate(
            user_text,
            target_language
        )

        response = (
            f"🌐 Source: {result.source_language}\n\n"
            f"🔤 Translation:\n"
            f"{result.translation}"
        )

        if result.expression:

            response += (
                f"\n\n💡 Expression:\n"
                f'"{result.expression}"\n'
                f"{result.expression_meaning}"
            )

        # Delete old bot translation
        previous_message_id = last_bot_messages.get(user_id)

        if previous_message_id:

            try:
                bot.delete_message(
                    chat_id,
                    previous_message_id
                )

            except Exception as error:
                print(
                    f"Could not delete previous translation: {error}"
                )

        # Delete translating message
        try:
            bot.delete_message(
                chat_id,
                translating_message.message_id
            )

        except Exception as error:
            print(
                f"Could not delete translating message: {error}"
            )

        # Send translation
        sent_message = bot.send_message(
            chat_id,
            response,
            reply_markup=translation_keyboard()
        )

        last_bot_messages[user_id] = sent_message.message_id

        user_messages[user_id].append(
            sent_message.message_id
        )

        # Delete user's message
        try:
            bot.delete_message(
                chat_id,
                message.message_id
            )

        except Exception as error:
            print(
                f"Could not delete user message: {error}"
            )

    except Exception as error:

        print(f"Translation error: {error}")

        try:
            bot.delete_message(
                chat_id,
                translating_message.message_id
            )
        except Exception:
            pass

        bot.send_message(
            chat_id,
            "❌ Something went wrong while translating."
        )


def main():
    print("LinguaAI is running...")
    bot.infinity_polling()


if __name__ == "__main__":
    main()
