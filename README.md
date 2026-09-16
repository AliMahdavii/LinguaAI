# 🌍 LinguaAI

**An AI-powered Telegram bot for natural and contextual text translation.**

LinguaAI is a Python-based Telegram bot that uses Large Language Models to translate text naturally while preserving **meaning, context, expressions, and tone**.

> 🌐 Break language barriers with AI.

---

## ✨ Features

* 🌍 **AI-powered translation**
* 🧠 **Automatic source-language detection**
* 💡 **Expression & idiom detection**
* ⚡ **Fast Telegram-based interaction**
* 🌐 **Multiple target languages**
* 🔄 **Change target language anytime**
* 🧹 **Clean chat experience**
* 🔐 **Environment-based API key management**

### Supported Languages

🇮🇷 Persian
🇬🇧 English
🇩🇪 German
🇫🇷 French
🇪🇸 Spanish

---

## 🏗️ Architecture

```text
Telegram User
      │
      ▼
Telegram Bot
      │
      ▼
Python Backend
      │
      ▼
Translator Service
      │
      ▼
AI Provider
      │
      ▼
Translation Result
      │
      ▼
Telegram Response
```

The project uses a **service-based architecture**, keeping Telegram handling and AI logic separated so the AI provider can be changed or extended later.

---

## 🛠️ Tech Stack

* 🐍 Python
* 🤖 pyTelegramBotAPI
* 🧠 LLM APIs
* 🗄️ SQLite
* 🔐 python-dotenv
* 🌱 Git & GitHub

---

## 📂 Project Structure

```text
LinguaAI/
│
├── src/
│   ├── services/
│   │   ├── gemini_service.py
│   │   └── translator_service.py
│   │
│   |── database.py
|   |── main.py
│   └── models.py
|
├── requirements.txt
├── .gitignore
└── .env
```

---

## ⚙️ Setup

Clone the repository:

```bash
git clone https://github.com/AliMahdavii/LinguaAI.git
cd LinguaAI
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

Run the bot:

```bash
python main.py
```

---

## 🚀 Roadmap

* [x] Telegram bot foundation
* [x] AI translation
* [x] Automatic language detection
* [x] Multiple target languages
* [x] Expression detection
* [x] User language persistence
* [x] Clean message management
* [ ] File translation
* [ ] Voice message translation
* [ ] Text-to-Speech integration
* [ ] Vocabulary / Dictionary features
* [ ] Production deployment

---

## 👨‍💻 Author

**Ali Mahdavi**

Computer Engineering Student
Interested in Python, Linux, Networking & Cybersecurity.

---

⭐ If you find LinguaAI interesting, consider giving the repository a star.
