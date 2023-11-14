from datetime import datetime
import psycopg2
import telebot
import os
from dotenv import load_dotenv

load_dotenv()
Bot_key = os.getenv("BOT_KEY")
bot = telebot.TeleBot(Bot_key)

ADD_HABIT_PLACE, ADD_HABIT_TIME, ADD_HABIT_PLEASANT, ADD_HABIT_FREQUENCY = range(4)


@bot.message_handler(commands=['start'])
def url(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton(text='Сайт проекта', url='https://github.com/AdoleHitlman/habits_project')
    markup.add(btn1)
    bot.send_message(message.from_user.id, "Добро пожаловать в бота по добавлению полезных привычек\n"
                                           "бот представляет собой трекер полезных привычек\n"
                                           "чтобы добавить привычку введите '/add_habit'"
                                           " посмотреть свои привычки можно через '/habits'"
                                           "\n,удалить их пожно с помощью '/delete_habit'"
                                           "По кнопке ниже можно перейти на сайт проекта", reply_markup=markup)


@bot.message_handler(commands=['add_habit'])
def add_habit(message):
    user_id = message.from_user.id

    # Запрашиваем первое поле - место привычки
    bot.send_message(user_id, 'Введите место привычки:')
    bot.register_next_step_handler(message, save_place)


def save_place(message):
    place = message.text
    user_id = message.from_user.id

    # Сохраняем место привычки в базе данных
    conn = psycopg2.connect(host='localhost', dbname='habits_project', user='postgres', password='1')
    cursor = conn.cursor()
    cursor.execute("UPDATE habits_habit SET place = %s WHERE telegram_id = %s::varchar", (place, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    # Запрашиваем второе поле - время привычки
    bot.send_message(user_id, 'Введите время привычки в формате HH:MM\nпример 22:22')
    bot.register_next_step_handler(message, save_time)


def save_time(message):
    time_str = message.text
    user_id = message.from_user.id

    try:
        # Преобразуем строку времени в объект datetime
        time = datetime.strptime(time_str, '%H:%M')

        # Сохраняем время привычки в базе данных
        conn = psycopg2.connect(host='localhost', dbname='habits_project', user='postgres', password='1')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE habits_habit SET time = %s WHERE telegram_id = %s::varchar", (time, user_id))
        conn.commit()
        cursor.close()
        conn.close()

        # Запрашиваем третье поле - является ли привычка приятной
        bot.send_message(user_id, 'Введите, является ли привычка приятной (да/нет):')
        bot.register_next_step_handler(message, save_is_pleasant)
    except ValueError:
        # Обрабатываем случай, когда введен некорректный формат времени
        bot.send_message(user_id, 'Неверный формат времени. Введите время в формате HH:MM\nпример 22:22')
        bot.register_next_step_handler(message, save_time)


def save_is_pleasant(message):
    is_pleasant_str = message.text.lower()
    user_id = message.from_user.id

    if is_pleasant_str == 'да':
        is_pleasant = True
    else:
        is_pleasant = False
        # Сохраняем информацию о том, является ли привычка приятной, в базе данных
    conn = psycopg2.connect(host='localhost', dbname='habits_project', user='postgres', password='1')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE habits_habit SET is_pleasant = %s WHERE telegram_id = %s::varchar",
                   (is_pleasant, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    # Запрашиваем четвертое поле - частоту привычки
    bot.send_message(user_id, 'Введите частоту привычки:')
    bot.register_next_step_handler(message, save_frequency)


def save_frequency(message):
    frequency = message.text
    user_id = message.from_user.id

    # Сохраняем частоту привычки в базе данных
    conn = psycopg2.connect(host='localhost', dbname='habits_project', user='postgres', password='1')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE habits_habit SET frequency = %s, telegram_id = %s::varchar", (frequency, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    # Завершаем процесс добавления привычки
    bot.send_message(user_id, 'Привычка успешно добавлена!\n'
                              ' посмотреть свои привычки можно через "/habits"'
                              '\n,удалить их пожно с помощью "/delete_habit"')


@bot.message_handler(commands=['habits'])
def get_habits(message):
    conn = psycopg2.connect(host='localhost', dbname='habits_project', user='postgres', password='1')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habits_habit")
    habits = cursor.fetchall()
    response = "Ваши привычки:\n"
    for habit in habits:
        response += f"- {habit[1]}\n"
    bot.reply_to(message, response)
    cursor.close()
    conn.close()


@bot.message_handler(commands=['delete_habit'])
def delete_habit(message):
    # Получение имени привычки, которую нужно удалить
    habit_name = message.text.split(' ', 1)[1]

    # Подключение к базе данных
    conn = psycopg2.connect(host='localhost', dbname='habits_project', user='postgres', password='1')

    # Создание курсора
    cursor = conn.cursor()

    # Поиск привычки в базе данных
    cursor.execute("SELECT * FROM habits_habit WHERE name = %s", (habit_name,))
    habit = cursor.fetchone()

    if habit:
        # Удаление привычки
        cursor.execute("DELETE FROM habits_habit WHERE name = %s", (habit_name,))
        conn.commit()
        response = f"Привычка \"{habit_name}\" удалена успешно!"
    else:
        response = f"Привычки \"{habit_name}\" не существует."

    # Отправка сообщения с результатом удаления
    bot.reply_to(message, response)

    # Закрытие соединения
    cursor.close()
    conn.close()


bot.polling(none_stop=True)
