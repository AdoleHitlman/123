from rest_framework import serializers
from .models import Habit
from habits.validators import Related_or_Award_HabitValidator, Time_limit_seconds_HabitValidator, \
    Related_is_pleasant_habit_HabitValidator, Pleasant_HabitValidator, Time_period_days_HabitValidator
class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [Related_or_Award_HabitValidator(),
                      Time_limit_seconds_HabitValidator(),
                      Related_is_pleasant_habit_HabitValidator(),
                      Pleasant_HabitValidator(),
                      Time_period_days_HabitValidator()
                      ]