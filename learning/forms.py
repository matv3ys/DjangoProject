"""
Forms
"""

import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Word

class WordForm(forms.ModelForm):
    """
    Form wor word editing
    """
    class Meta:
        """
        Meta information
        """
        model = Word
        fields = ['english_word', 'translation', 'transcription', 'example_sentence', 'difficulty']
        widgets = {
            'english_word': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Enter English word'}),
            'translation': forms.TextInput(attrs={'class': 'form-control',
                                                  'placeholder': 'Введите перевод'}),
            'transcription': forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder': '[trænˈskrɪpʃən]'}),
            'example_sentence': forms.Textarea(attrs={'class': 'form-control',
                                                      'rows': 3}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_english_word(self):
        """
        Custom validation
        """
        word = self.cleaned_data.get('english_word')
        # Проверка: только латиница, дефисы и пробелы
        if not re.match(r'^[a-zA-Z\s\-]+$', word):
            raise ValidationError("Используйте только английские буквы.")
        return word.lower() # Сохраняем всегда в нижнем регистре

class ExportForm(forms.Form):
    """
    PDF export form
    """
    DIFFICULTY_CHOICES = [
        ('all', 'Все уровни'),
        ('easy', 'Easy (Легкие)'),
        ('medium', 'Medium (Средние)'),
        ('hard', 'Hard (Сложные)'),
    ]

    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        label="Сложность слов",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    include_examples = forms.BooleanField(
        required=False,
        initial=True,
        label="Включить примеры предложений",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class QuizForm(forms.Form):
    """
    Form to train yourself
    """
    answer = forms.CharField(
        label="Ваш ответ",
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'autocomplete': 'off', 'autofocus': 'on'})
    )

    def clean_answer(self):
        """
        Clean
        """
        answer = self.cleaned_data.get('answer')
        if not answer:
            raise ValidationError("Поле не может быть пустым.")
        return answer.strip().lower()
