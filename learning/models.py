from django.db import models
from django.core.validators import MinLengthValidator

class Word(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    english_word = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2, "Слово слишком короткое")],
        verbose_name="Слово на английском"
    )
    translation = models.CharField(
        max_length=100,
        verbose_name="Перевод"
    )
    transcription = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Транскрипция"
    )
    example_sentence = models.TextField(
        blank=True,
        verbose_name="Пример предложения"
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='easy',
        verbose_name="Уровень сложности"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.english_word} - {self.translation}"

    class Meta:
        verbose_name = "Слово"
        verbose_name_plural = "Слова"
        ordering = ['-created_at']