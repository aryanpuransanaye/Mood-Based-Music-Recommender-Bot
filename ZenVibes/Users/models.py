from django.db import models

class TelegramUser(models.Model):
    bot_user_id = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class MoodType(models.Model):
    name = models.CharField(max_length=50, unique=True)

class UserMood(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    mood = models.ForeignKey(MoodType, on_delete=models.CASCADE)
    mood_description = models.TextField(null=True, blank=True)
    mood_date = models.DateTimeField(auto_now_add=True) 
