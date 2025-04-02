# learning/views.py
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from .models import Word
from .forms import WordForm, ExportForm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas  # Для PDF
from reportlab.pdfbase.ttfonts import TTFont # Кириллица

# Список слов
def word_list(request):
    words = Word.objects.all()
    return render(request, 'learning/word_list.html', {'words': words})


# Детальная страница
def word_detail(request, pk):
    word = get_object_or_404(Word, pk=pk)
    return render(request, 'learning/word_detail.html', {'word': word})


# Создание слова
def word_create(request):
    if request.method == "POST":
        form = WordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('word_list')
    else:
        form = WordForm()
    return render(request, 'learning/word_form.html', {'form': form, 'title': 'Добавить новое слово'})

# Редактирование слова
def word_update(request, pk):
    word = get_object_or_404(Word, pk=pk)
    if request.method == "POST":
        form = WordForm(request.POST, instance=word)
        if form.is_valid():
            form.save()
            return redirect('word_detail', pk=word.pk)
    else:
        form = WordForm(instance=word)
    return render(request, 'learning/word_form.html', {'form': form, 'title': 'Редактировать слово'})

# Удаление слова
def word_delete(request, pk):
    word = get_object_or_404(Word, pk=pk)
    if request.method == "POST":
        word.delete()
        return redirect('word_list')
    return render(request, 'learning/word_confirm_delete.html', {'word': word})

# Экспорт в PDF
def export_pdf(request):
    if request.method == "POST":
        form = ExportForm(request.POST)
        if form.is_valid():
            difficulty = form.cleaned_data['difficulty']

            # Настройка шрифта для кириллицы
            font_path = os.path.join(settings.BASE_DIR, 'learning/fonts', 'DejaVuSans.ttf')
            pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="vocabulary.pdf"'

            p = canvas.Canvas(response)
            p.setFont("DejaVuSans", 16)  # Используем наш шрифт
            p.drawString(100, 800, f"Список слов ({difficulty})")

            y = 750
            p.setFont("DejaVuSans", 12)

            words = Word.objects.all() if difficulty == 'all' else Word.objects.filter(difficulty=difficulty)

            for word in words:
                p.drawString(100, y, f"{word.english_word} — {word.translation}")
                y -= 20
                if y < 50:
                    p.showPage()
                    p.setFont("DejaVuSans", 12)
                    y = 800

            p.showPage()
            p.save()
            return response
    else:
        form = ExportForm()
    return render(request, 'learning/export_form.html', {'form': form, 'title': 'Настройка экспорта'})