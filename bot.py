from os import environ

from dotenv import load_dotenv
import telebot

from generate_lyrics import generate_by_prompt

load_dotenv()
TOKEN = environ.get('TOKEN')

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    song = generate_by_prompt(message.text)
    bot.send_message(message.from_user.id, song)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
