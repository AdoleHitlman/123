from rest_framework.serializers import ValidationError


class Related_or_Award_HabitValidator:
    """Исключить одновременный выбор связанной привычки и указания вознаграждения"""
    def __call__(self, attrs):
        related_habit = attrs.get('related_habit')
        award = attrs.get('award')

        if related_habit and award:
            raise ValidationError('Вы должны указать либо связанную привычку, либо признак приятной привычки, '
                                  'или указать принак приятной привычки')


class Time_limit_seconds_HabitValidator:
    """Время выполнения должно быть не больше 120 секунд."""
    def __call__(self, attrs):
        time_limit_seconds = attrs.get('time_limit_seconds')
        if time_limit_seconds > 120:
            raise ValidationError('Время на выполнение не более 2х минут')


class Related_is_pleasant_habit_HabitValidator:
    """В связанные привычки могут попадать только привычки с признаком приятной привычки"""
    def __call__(self, attrs):
        related_habit = attrs.get('related_habit')
        if related_habit and not related_habit.is_pleasant_habit:
            raise ValidationError('В связанные привычки могут попадать только привычки с признаком приятной привычки')
        return attrs


class Pleasant_HabitValidator:
    """У приятной привычки не может быть вознаграждения или связанной привычки."""
    def __call__(self, attrs):
        is_pleasant_habit = attrs.get('is_pleasant_habit')
        related_habit = attrs.get('related_habit')
        award = attrs.get('award')
        if is_pleasant_habit:
            if related_habit or award:
                raise ValidationError(
                    'У приятной привычки не может быть вознаграждения или связанной привычки.')


class Time_period_days_HabitValidator:
    """Нельзя выполнять привычку реже, чем 1 раз в 7 дней"""
    def __call__(self, attrs):
        time_period_days = attrs.get('time_period_days')
        if time_period_days > 7:
            raise ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней')