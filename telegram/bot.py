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
        self.ask_user_mood_detail_buttons = {'I want':'mood_detail_yes', "I Don't Want":'mood_detail_no'}
        
        self.user_temp_moods = {}
        self.waiting_for_detail = {}

        self.setup_handlers()

    def send_main_menu(self, message, text='Choose an option below:'):

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[KeyboardButton(name) for name in self.menu_buttons_name])

        self.bot.send_message(message.chat.id, text, reply_markup=keyboard)

    def ask_user_mood_detail(self, message):

        inline_keyboard = InlineKeyboardMarkup(row_width=2)
        inline_keyboard.add(*[InlineKeyboardButton(text = key, callback_data = value) for key, value in self.ask_user_mood_detail_buttons.items()])

        self.bot.send_message(message.chat.id, 'Do You Want Tell Me About Your Mood?', reply_markup=inline_keyboard)

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

    def save_user_mood_and_send_music_and_quote(self, mood, description, user_id, chat_id):

        from views.recommendation_views import get_recommendations
        from views.get_or_create_user_mood import create_user_mood

        create_user_mood(mood, description, str(user_id))

        audio_file, caption, music_title, music_artist = get_recommendations(mood)

        if audio_file:
            self.bot.send_audio(chat_id, audio=audio_file, caption=caption, title=music_title, performer=music_artist, parse_mode="Markdown")
        else:
            self.bot.send_message(chat_id, '❌ There is no music for this mood')

    def setup_handlers(self):

        @self.bot.message_handler(commands=['start'])
        def start_handler(message):
            user_firsT_name = message.from_user.first_name
            text = f'Hi {user_firsT_name} 🥰\nHow are you doing right now?'
            self.send_main_menu(message, text)

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
        def ask_user_mood(message):
            
            chat_id = message.chat.id
            user_mood = re.sub(r'[^\w\s]', '', message.text).strip()
            self.user_temp_moods[chat_id] = user_mood
            self.ask_user_mood_detail(message) 


        @self.bot.callback_query_handler(func=lambda call:call.data in ['mood_detail_yes', 'mood_detail_no'])
        def ask_detail(call):
            
            chat_id = call.message.chat.id
            user_id = call.from_user.id
            user_mood = self.user_temp_moods.get(chat_id)

            if call.data == 'mood_detail_yes':
                self.bot.send_message(chat_id, 'Feel free to tell me more about your mood 💬')
                self.waiting_for_detail[chat_id] = (user_mood, user_id)
            else:
                self.save_user_mood_and_send_music_and_quote(user_mood, '', chat_id, user_id)
                self.user_temp_moods.pop(chat_id, None)
        

        @self.bot.message_handler(func=lambda m: m.chat.id in self.waiting_for_detail)
        def receive_detail(message):
            chat_id = message.chat.id
            mood, user_id = self.waiting_for_detail.pop(chat_id)
            mood_description = message.text
            self.save_user_mood_and_send_music_and_quote(mood, mood_description, chat_id, user_id)
            self.user_temp_moods.pop(chat_id, None)


        @self.bot.message_handler(func=lambda m: m.text == 'mood history')
        def send_mood_history(message):
            from views.get_or_create_user_mood import get_mood_history
            from datetime import datetime

            result = get_mood_history(str(message.from_user.id))

            if not result['ok']:
                reply = "Sorry, I couldn't retrieve your mood history at the moment. Please try again later."
                self.bot.send_message(message.chat.id, reply)
                return

            moods = result['data']
            if not moods:
                reply = "You haven't recorded any moods yet. Tap 'Choose your Mood' to get started 😊"
                self.bot.send_message(message.chat.id, reply)
                return

            lines = []
            for entry in moods:
                mood_name = entry.get('mood_name', 'Unknown')
                mood_date = entry.get('mood_date')
                mood_description = entry.get('mood_description', '')

                if mood_date:
                    try:
                        dt = datetime.fromisoformat(mood_date)
                        formatted_date = dt.strftime("%B %d, %Y at %H:%M")
                    except Exception:
                        formatted_date = mood_date
                else:
                    formatted_date = "Unknown date"

                if not mood_description:
                    mood_description = "No additional notes were added."

                line = f"🗓 On *{formatted_date}*, you felt *{mood_name}*."
                line += f"\n📝 Description: _{mood_description}_\n"
                lines.append(line)

            max_length = 4000
            current_message = ""

            for line in lines:
                if len(current_message) + len(line) < max_length:
                    current_message += line + "\n\n"
                else:
                    self.bot.send_message(message.chat.id, current_message.strip(), parse_mode="Markdown")
                    current_message = line + "\n\n"

            if current_message:
                self.bot.send_message(message.chat.id, current_message.strip(), parse_mode="Markdown")


    def run(self):
        self.bot.polling()


if __name__ == '__main__':


    TOKEN = config('TELEGRAM_BOT_TOKEN')
    mood_bot = Bot(TOKEN)
    mood_bot.run()

