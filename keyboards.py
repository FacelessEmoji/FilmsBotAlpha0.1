import telebot


def admin_menu():
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)

    buttons = [
        telebot.types.InlineKeyboardButton("Добавить фильм в базу данных 📁", callback_data="addFilmAdmin"),
        telebot.types.InlineKeyboardButton("Показать все фильмы из базы данных 📁", callback_data="FilmsAdmin"),
    ]

    keyboard.add(*buttons)

    return keyboard
