from django.contrib import admin
from .models import TelegramUser, MoodType, UserMood
# Register your models here.

@admin.register(TelegramUser)
class TelegramUSerAdmin(admin.ModelAdmin):
    
    list_display = ['bot_user_id', 'created_at']
    list_filter = ['bot_user_id', 'created_at']
    search_fields = [' bot_user_id']

@admin.register(MoodType)
class MoodTypeAdmin(admin.ModelAdmin):

    list_display = ['name']
    list_filter = ['name']


@admin.register(UserMood)
class UserMoodAdmin(admin.ModelAdmin):

    list_display = ['user', 'mood', 'mood_description', 'mood_date']
    list_filter = ['user', 'mood']
    search_fields = ['user', 'mood']
    list_per_page = 20





    