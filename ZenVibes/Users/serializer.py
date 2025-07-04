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
    mood = serializers.SerializerMethodField()

    class Meta:
        model = UserMood
        fields = ['user', 'mood', 'mood_date']
    
    def get_mood(self, obj):
        return obj.mood.name

