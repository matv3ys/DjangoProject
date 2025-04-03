"""
admin
"""

from django.contrib import admin
from .models import Word

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    """
    word admin
    """
    list_display = ('english_word', 'translation', 'difficulty', 'created_at')
    list_filter = ('difficulty',)
    search_fields = ('english_word', 'translation')
