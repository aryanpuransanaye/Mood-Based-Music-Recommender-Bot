# MoodMaster Bot

A smart Telegram bot that helps users manage their moods by recommending music and providing personalized motivational quotes.

---

## Features

* 🎵 Suggests music tailored to your current mood.
* 💬 Provides motivational quotes based on your mood.
* 🤖 Built with Python, TeleBot (pyTelegramBotAPI), and Django.
* 🧑‍💻 Easy to extend and customize.
* 🔄 Supports interactive menus and mood history.

---

## Getting Started

### Prerequisites

* Python 3.8+
* Telegram bot token (from [BotFather](https://t.me/BotFather))

### Installation

1. Clone the repository:

```bash
git clone https://github.com/aryanpuransanaye/Mood-Based-Music-Recommender-Bot.git
cd Mood-Based-Music-Recommender-Bot
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your API keys in the code or environment variables:

* `YOUR_TELEGRAM_BOT_TOKEN`

### Usage

Run the bot:

```bash
python telegram/bot.py
```

---

## Project Structure

```
Mood-Based-Music-Recommender-Bot/
│
├── ZenVibes/                      # Backend Django project and apps
│   ├── Users/                     # User management and moods app
│   ├── Music/                     # Music-related app
│   ├── Quotes/                    # Quotes management app
│   ├── MoodFusion/                # Mood fusion and logic app
│   ├── ZenVibes/                  # Core Django app (settings, URLs, etc.)
│   ├── load_quotes.py             # Script to load quotes data
│   └── manage.py                  # Django management script
│
├── telegram/                      # Telegram bot files
│   ├── bot.py                    # Main bot logic and handlers
│   ├── text_message.py           # Predefined bot text messages
│   └── views/                    # API views for bot communication
│       ├── get_or_create_user_mood.py
│       └── recommendation_views.py
│
└── requirements.txt               # Python dependencies
```

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## Bot Usage

To start interacting with the bot, you can visit the Telegram link: [@moodbasemusic\_bot](https://t.me/moodbasemusic_bot)
