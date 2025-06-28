import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import requests

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
        def send_quote(message):

            user_mood = str((message.text).split()[1])

            url = 'https://aryanpuransanaye.pythonanywhere.com/api/recommendation/'
            data = {
                'mood': user_mood
            }

            try:
                response = requests.post(url, json=data)
                response.raise_for_status()
                result = response.json()

                quote_data = result.get('quote',{})
                music_data = result.get('music',{})

                caption = f"💬 *{quote_data.get('text', 'No qoute')}*\n\n— _{quote_data.get('author', 'Unknown')}_"


                music_url = music_data.get('file_url')
                response = requests.get(music_url, timeout=60)
                audio_data = response.content


                if audio_data:
                    self.bot.send_audio(message.chat.id, audio_data, caption=caption, parse_mode="Markdown")
                else:
                    self.bot.send_message(message.chat.id, "❌ There is no music for this mood")

            except requests.exceptions.HTTPError as errh:
                print("❌ HTTP Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("❌ Connection Error:", errc)
            except requests.exceptions.Timeout as errt:
                print("❌ Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("❌ Other Error:", err)


    def run(self):
        self.bot.polling()


if __name__ == '__main__':


    TOKEN = '7798028137:AAE24kOhRwB6cx5YR93uGyL8H2D43dVTndE'
    mood_bot = Bot(TOKEN)
    mood_bot.run()

