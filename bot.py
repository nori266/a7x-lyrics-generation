from os import environ

from dotenv import load_dotenv
import telebot

from generate_lyrics import generate_by_prompt

load_dotenv()
TOKEN = environ.get('TOKEN')

bot = telebot.TeleBot(TOKEN)

markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
itembtn1 = telebot.types.KeyboardButton('Hail to the king')
itembtn2 = telebot.types.KeyboardButton('I am dying')
itembtn3 = telebot.types.KeyboardButton('God')
markup.add(itembtn1, itembtn2, itembtn3)


@bot.message_handler(commands=['start', 'help'])
def command_help(message):
    bot.send_message(
        message.from_user.id,
        "Hi! Text me a prompt and I will generate lyrics in the style of Avenged Sevenfold special for you! "
        "Try one of the buttons or type your own prompt.",
        reply_markup=markup
    )


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    uid = message.from_user.id
    bot.send_chat_action(uid, 'typing')
    song = generate_by_prompt(message.text)
    bot.send_message(uid, song, reply_markup=markup)
    print("MESSAGE", message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
