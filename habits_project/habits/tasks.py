import os
import telebot
from celery import shared_task

from habits.models import Habit

Bot_key = os.getenv("BOT_KEY")
bot = telebot.TeleBot(Bot_key)


@shared_task
def send_reminder_telegram_chat(habit_id):
    # Retrieve habit information by its ID
    habit = Habit.objects.get(id=habit_id)
    bot.send_message(chat_id=habit.user.telegram_id, text=f"Напоминание: {habit.name}")


