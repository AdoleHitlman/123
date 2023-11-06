from users.models import User
from django.db import models

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.CharField(max_length=100)
    time = models.DateTimeField()
    action = models.CharField(max_length=100)
    is_pleasant = models.BooleanField()
    related_habit = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    frequency = models.CharField(max_length=20)
    reward = models.CharField(max_length=100, null=True, blank=True)
    time_to_complete = models.IntegerField()
    is_public = models.BooleanField()
    telegram_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.action