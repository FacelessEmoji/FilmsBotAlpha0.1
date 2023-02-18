import telebot
import sqlite3
from keyboards import *
from config import *
from db import BotDB


def is_sub(channel_id, user_id):
    for i in status:
        if i == bot.get_chat_member(channel_id, user_id).status:
            return True


BotDB = BotDB('server.db')
bot = telebot.TeleBot(token)

# BotDB.sql.execute("DROP table films")
# BotDB.db.commit()

@bot.message_handler(commands=["start"])
def main(message):
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEDSVphkhEeu8dhcAg1Lug71Ng4OHcRKQAC2A8AAkjyYEsV-8TaeHRrmCIE")
    bot.send_message(message.chat.id, "Введите номер из видео для того чтобы узнать название фильма:")


@bot.message_handler(commands=['admin'])
def admin(message):
    if message.chat.id in admins:
        bot.send_message(message.chat.id, "Выберите то, что вас интересует.⬇️", reply_markup=admin_menu())


@bot.message_handler(content_types=["text"])
def main(message):
    flag = True
    if str(message.text).isdigit() and len(str(message.text)) == 4:
        for i in channels.keys():
            if not is_sub(channels[i], message.chat.id):
                flag = False
                bot.send_message(message.chat.id, "Для использования бота,"
                                                  "Вы должны подписаться на все каналы ниже."
                                                  " Перейти на каналы можно по нажатию кнопок.⬇",
                                 reply_markup=menu(message))
                bot.send_message(message.chat.id, "После подписки нажмите на: \n"
                                                  "  Проверить подписки ✅ ")
                break
        if flag:
            if BotDB.sql.execute(f"SELECT film FROM films WHERE filmcode={message.text}").fetchone():
                bot.send_message(message.chat.id,
                                 "Название фильма: \n" + str(BotDB.get_film_for_user(message.text))[2:-3])


def menu(message):
    buttons = []
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    for i in channels.keys():
        if not is_sub(channels[i], message.chat.id):
            buttons.append(
                telebot.types.InlineKeyboardButton("Подпишитесь на канал 📋", url=links[i]))
    buttons.append(telebot.types.InlineKeyboardButton("Проверить подписки ✅", callback_data="updated_menu"))

    keyboard.add(*buttons)

    return keyboard


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'addFilmAdmin':
        msg = bot.send_message(call.message.chat.id, 'Введите название фильма и код через ==.\n'
                                                     'Пример: "Аватар == 0102"')
        bot.register_next_step_handler(msg, get_film)
    elif call.data == "FilmsAdmin":
        for value in BotDB.get_all_films():
            bot.send_message(call.message.chat.id, "film: " + value[0] + "\ncode: " + str(value[1]))
    elif call.data == "updated_menu":
        flag = True
        for i in channels.keys():
            if not is_sub(channels[i], call.message.chat.id):
                flag = False
                bot.send_message(call.message.chat.id, "Подпишитесь на оставшиеся каналы!",
                                 reply_markup=menu(call.message))
                bot.send_message(call.message.chat.id, "После подписки нажмите на: \n"
                                                       "  Проверить подписки ✅ ")
                break
        if flag:
            bot.send_message(call.message.chat.id, "Теперь вы можете узнать название фильма. "
                                                   "Введите номер из видео для того чтобы узнать название фильма:")


def get_film(message):
    if len(message.text.split("==")) == 2:
        film = message.text.split("==")[0].strip()

        code = message.text.split("==")[1].strip()

        if not code.isdigit() and len(code) == 4 and len(film) != 0:
            bot.send_message(message.chat.id, "Данные не валидны!", reply_markup=admin_menu())
            return
        else:
            code = int(code.strip())
            BotDB.add_film(film, code)
            bot.send_message(message.chat.id, "Фильм добавлен в базу данных!")


bot.polling()
