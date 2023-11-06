from django.core.exceptions import ValidationError

from habits.models import Habit


def validate_related_habit(value):
    habit = Habit.objects.get(pk=value)
    if habit.is_pleasant:
        if habit.reward is not None:
            raise ValidationError("Pleasant habits cannot have a reward.")
    else:
        if habit.related_habit is not None:
            raise ValidationError("Unpleasant habits cannot have a related habit.")

def validate_execution_time(value):
    if value > 120:
        raise ValidationError("Execution time should not exceed 120 seconds.")

def validate_related_habit(value):
    related_habit = Habit.objects.get(pk=value)
    if not related_habit.is_pleasant:
        raise ValidationError("Related habit should be a pleasant habit.")


def validate_pleasant_habit(value):
    habit = Habit.objects.get(pk=value)
    if habit.is_pleasant:
        if habit.reward is not None:
            raise ValidationError("Pleasant habits cannot have a reward.")
        if habit.related_habit is not None:
            raise ValidationError("Pleasant habits cannot have a related habit.")

from datetime import timedelta, date

def validate_habit_frequency(value):
    habit = Habit.objects.get(pk=value)
    last_execution_date = habit.last_execution_date
    current_date = date.today()
    if last_execution_date is not None and (current_date - last_execution_date) < timedelta(days=7):
        raise ValidationError("Habit should not be executed less frequently than once every 7 days.")