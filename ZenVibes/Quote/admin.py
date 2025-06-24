from django.contrib import admin
from .models import Quote

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):

    list_display = ('short_text', 'author', 'mood', 'created_at')
    list_filter = ('mood', 'author')
    search_fields = ('text', 'author')


    def short_text(self, obj):

        return obj.text[:50] + ('...' if len(obj.text) > 50 else '')
    
