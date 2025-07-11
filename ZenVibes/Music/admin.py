from django.contrib import admin
from .models import Music


@admin.register(Music)
class QuoteAdmin(admin.ModelAdmin):

    list_display = ('title', 'artist', 'mood', 'audio_file', 'created_at')
    readonly_fields = ('title', 'artist')
    list_filter = ('mood', 'artist')
    search_fields = ('title', 'artist', 'mood')

