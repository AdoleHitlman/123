import telebot
from celery import shared_task

from habits.models import Habit

bot = telebot.TeleBot('6326493689:AAHhVJeDPe2bTpRMgkuYKMWYdLwHg-Mji2A')


@shared_task
def send_reminder_telegram_chat(habit_id):
    # Retrieve habit information by its ID
    habit = Habit.objects.get(id=habit_id)
    bot.send_message(chat_id=habit.user.telegram_id, text=f"Напоминание: {habit.name}")


