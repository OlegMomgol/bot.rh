import telebot
import requests
from telebot import types

API_TOKEN = ""
bot = telebot.TeleBot(API_TOKEN)

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Поиск книги")
    button2 = types.KeyboardButton("Поиск автора")
    button3 = types.KeyboardButton("Помощь")
    markup.add(button1, button2, button3)
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите действие:", reply_markup=main_menu())


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "Поиск книги":
        bot.send_message(message.chat.id, "Введите название книги или ISBN:")
        bot.register_next_step_handler(message, search_book)
    elif message.text == "Поиск автора":
        bot.send_message(message.chat.id, "Введите имя автора:")
        bot.register_next_step_handler(message, search_author)
    elif message.text == "Помощь":
        bot.send_message(message.chat.id, "Это бот для поиска книг и авторов. Используйте кнопки для поиска.")



def search_book(message):
    query = message.text
    response = requests.get(f'https://openlibrary.org/search.json?q={query}')

    if response.status_code == 200:
        data = response.json()
        if data['docs']:
            results = []
            for book in data['docs'][:5]:  # Ограничим вывод 5 результатами
                title = book.get('title', 'Неизвестно')
                authors = ', '.join(book.get('author_name', ['Неизвестно']))
                results.append(f"Название: {title}\nАвтор(ы): {authors}\n")
            bot.send_message(message.chat.id, "\n".join(results))
        else:
            bot.send_message(message.chat.id, "Книги не найдены.")
    else:
        bot.send_message(message.chat.id, "Произошла ошибка при поиске книги.")

def search_author(message):
    query = message.text
    response = requests.get(f'https://openlibrary.org/search/authors.json?q={query}')

    if response.status_code == 200:
        data = response.json()
        if data['docs']:
            results = []
            for author in data['docs'][:5]:  # Ограничим вывод 5 результатами
                name = author.get('name', 'Неизвестно')
                works_count = author.get('work_count', 0)
                results.append(f"Автор: {name}\nКоличество работ: {works_count}\n")
            bot.send_message(message.chat.id, "\n".join(results))
        else:
            bot.send_message(message.chat.id, "Авторы не найдены.")
    else:
        bot.send_message(message.chat.id, "Произошла ошибка при поиске автора.")


bot.polling()
