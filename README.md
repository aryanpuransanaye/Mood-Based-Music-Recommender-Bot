# MoodMaster Bot

A smart Telegram bot that helps users manage their moods by recommending music and providing personalized motivational quotes using OpenAI’s GPT API.

---

## Features

* 🎵 Suggests music tailored to your current mood.
* 💬 Provides motivational quotes based on your mood.
* 🤖 Built with Python, TeleBot (pyTelegramBotAPI), and OpenAI’s GPT.
* 🧑‍💻 Easy to extend and customize.
* 🔄 Supports interactive menus and mood history (planned).

---

## Getting Started

### Prerequisites

* Python 3.8+
* Telegram bot token (from [BotFather](https://t.me/BotFather))
* OpenAI API key (from [OpenAI](https://platform.openai.com/account/api-keys))

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your_username/moodmaster-bot.git
cd moodmaster-bot
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your API keys in the code or environment variables:

* `YOUR_TELEGRAM_BOT_TOKEN`
* `YOUR_OPENAI_API_KEY`

### Usage

Run the bot:

```bash
python bot.py
```

---

## Project Structure

* `bot.py` — Main Telegram bot logic and handlers.
* `openai_api.py` — Integration with OpenAI API for motivational quotes.
* `mood_handler.py` — Mood selection and related features.
* `README.md` — This documentation file.

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---
