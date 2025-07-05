from rest_framework import serializers
from .models import UserMood, TelegramUser, MoodType

class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['bot_user_id']

class MoodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodType
        fields = ['name']

class UserMoodSerializer(serializers.ModelSerializer):
    mood_name = serializers.CharField(source='mood.name', read_only=True)

    class Meta:
        model = UserMood
        fields = ['user', 'mood', 'mood_name', 'mood_date']