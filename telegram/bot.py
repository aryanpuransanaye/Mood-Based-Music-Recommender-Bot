import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from decouple import config
import re

class Bot:

    def __init__(self, token):

        self.bot = telebot.TeleBot(token)

        self.menu_buttons_name = ['Choose your Mood', 'Bot Info', 'mood history', 'Creator']
        self.mood_buttons_name = ['😁 Happy', '😞 Sad', '😪 Tired', '😰 Stressed', '🥰 In Love']
        self.creator_buttons_name = {'GitHub':'https://github.com/aryanpuransanaye', 'Linkdin':'https://www.linkedin.com/in/aryan-puransanaye/'}

        self.setup_handlers()

    def send_main_menu(self, message):

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[KeyboardButton(name) for name in self.menu_buttons_name])

        self.bot.send_message(message.chat.id, 'Choos an option below: ', reply_markup=keyboard)

    def send_mood_menu(self, message):

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[KeyboardButton(name) for name in self.mood_buttons_name])
        keyboard.add( '🔙 Back to Main Menu')

        self.bot.send_message(message.chat.id, 'Choos your mood: ', reply_markup=keyboard)

    def send_creator_menu(self, message):

        inline_keyboard = InlineKeyboardMarkup(row_width=2)
        inline_keyboard.add(*[InlineKeyboardButton(text = key, url = value) for key, value in self.creator_buttons_name.items()])

        from text_message import creator_text
        self.bot.send_message(message.chat.id, creator_text, reply_markup=inline_keyboard)

    def setup_handlers(self):

        @self.bot.message_handler(commands=['start'])
        def start_handler(message):
            self.send_main_menu(message)

        @self.bot.message_handler(func=lambda m: m.text == 'Choose your Mood')
        def mood_menu_handler(message):
            self.send_mood_menu(message)

        @self.bot.message_handler(func=lambda m:m.text == 'Bot Info')
        def info_message_handler(message):
            from text_message import info_text
            self.bot.send_message(message.chat.id, info_text)

        @self.bot.message_handler(func=lambda m:m.text == 'Creator')
        def creator_menu_handler(message):
            self.send_creator_menu(message)

        @self.bot.message_handler(func=lambda m:m.text == '🔙 Back to Main Menu')
        def main_menu_handler(message):
            self.send_main_menu(message)

        @self.bot.message_handler(func=lambda m:m.text in ['😁 Happy', '😞 Sad', '😪 Tired', '😰 Stressed', '🥰 In Love'])
        def send_quote_music(message):
            from views.recommendation_views import get_recommendations
            from views.get_or_creat_user_mood import create_user_mood

            user_mood = re.sub(r'[^\w\s]', '', message.text).strip()

            create_user_mood(user_mood, str(message.from_user.id))

            audio_file, caption = get_recommendations(user_mood)

            if audio_file:
                self.bot.send_audio(message.chat.id, audio_file, caption=caption, parse_mode="Markdown")
            else:
                self.bot.send_message(message.chat.id, "❌ There is no music for this mood")

        @self.bot.message_handler(func=lambda m:m.text == 'mood history')
        def send_mood_history(message):
            from views.get_or_creat_user_mood import get_mood_history
            
            result = get_mood_history(str(message.from_user.id))
            
            if not result['ok']:
                reply = "Sorry, couldn't fetch your mood history."
            else:
                moods = result['data']
                if not moods:
                    reply = "You don't have any mood history yet."
                else:
                    lines = []
                    for entry in moods:
                        mood_name = entry.get('mood', 'Unknown')
                        mood_date = entry.get('mood_date')
                        
                        if mood_date:
                            from datetime import datetime
                            try:
                                dt = datetime.fromisoformat(mood_date)
                                formatted_date = dt.strftime("%B %d, %Y at %H:%M")
                            except Exception:
                                formatted_date = mood_date
                        else:
                            formatted_date = "Unknown date"
                        
                        lines.append(f"On {formatted_date}, you felt *{mood_name}*.")
                    
                    reply = "\n".join(lines)
            
            self.bot.send_message(message.chat.id, reply, parse_mode="Markdown")

    
    def run(self):
        self.bot.polling()

if __name__ == '__main__':


    TOKEN = config('TELEGRAM_BOT_TOKEN')
    mood_bot = Bot(TOKEN)
    mood_bot.run()

