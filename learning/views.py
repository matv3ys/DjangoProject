"""
views
"""

import os
import random
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas  # Для PDF
from reportlab.pdfbase.ttfonts import TTFont # Кириллица
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from .models import Word
from .forms import WordForm, ExportForm, QuizForm

# Список слов
def word_list(request):
    """
    word list
    """
    words = Word.objects.all()
    return render(request, 'learning/word_list.html', {'words': words})


# Детальная страница
def word_detail(request, pk):
    """
    word detail
    """
    word = get_object_or_404(Word, pk=pk)
    return render(request, 'learning/word_detail.html', {'word': word})


# Создание слова
def word_create(request):
    """
    word create
    """
    if request.method == "POST":
        form = WordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('word_list')
    else:
        form = WordForm()
    return render(request, 'learning/word_form.html',
                  {'form': form, 'title': 'Добавить новое слово'})

# Редактирование слова
def word_update(request, pk):
    """
    word update
    """
    word = get_object_or_404(Word, pk=pk)
    if request.method == "POST":
        form = WordForm(request.POST, instance=word)
        if form.is_valid():
            form.save()
            return redirect('word_detail', pk=word.pk)
    else:
        form = WordForm(instance=word)
    return render(request, 'learning/word_form.html',
                  {'form': form, 'title': 'Редактировать слово'})

# Удаление слова
def word_delete(request, pk):
    """
    word delete
    """
    word = get_object_or_404(Word, pk=pk)
    if request.method == "POST":
        word.delete()
        return redirect('word_list')
    return render(request, 'learning/word_confirm_delete.html', {'word': word})

# Экспорт в PDF
def export_pdf(request):
    """
    export pdf
    """
    if request.method == "POST":
        form = ExportForm(request.POST)
        if form.is_valid():
            difficulty = form.cleaned_data['difficulty']

            # Настройка шрифта для кириллицы
            font_path = os.path.join(settings.BASE_DIR, 'learning/fonts', 'DejaVuSans.ttf')
            pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="vocabulary.pdf"'

            p = canvas.Canvas(response)
            p.setFont("DejaVuSans", 16)  # Используем наш шрифт
            p.drawString(100, 800, f"Список слов ({difficulty})")

            y = 750
            p.setFont("DejaVuSans", 12)

            words = Word.objects.all() if difficulty == 'all' else \
                Word.objects.filter(difficulty=difficulty)

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
    return render(request, 'learning/export_form.html',
                  {'form': form, 'title': 'Настройка экспорта'})


def quiz_view(request):
    """
    quiz view
    """
    # 1. Инициализация счета
    if 'score' not in request.session:
        request.session['score'] = 0

    # Получаем ID слова, на которое пользователь отвечает сейчас
    current_word_id = request.session.get('quiz_word_id')
    feedback = None
    correct_answer = None

    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data['answer']
            word = get_object_or_404(Word, id=current_word_id)

            if user_answer.lower() == word.translation.lower().strip():
                request.session['score'] += 1
                feedback = "correct"
            else:
                feedback = "wrong"
                correct_answer = word.translation

            # Сохраняем это слово как "последнее пройденное", чтобы не повторить его сразу
            request.session['last_word_id'] = current_word_id
            # Удаляем текущее слово из сессии, чтобы при следующем GET выбралось новое
            if 'quiz_word_id' in request.session:
                del request.session['quiz_word_id']
    else:
        # GET-запрос: Выбираем новое слово
        form = QuizForm()
        last_word_id = request.session.get('last_word_id')

        # Исключаем последнее слово из выборки
        all_words = Word.objects.all()
        if all_words.count() > 1:
            words_pool = all_words.exclude(id=last_word_id)
        else:
            words_pool = all_words

        if words_pool.exists():
            new_word = random.choice(list(words_pool))
            request.session['quiz_word_id'] = new_word.id
            current_word_id = new_word.id
        else:
            return render(request, 'learning/quiz.html',
                          {'error': 'Добавьте хотя бы одно слово в словарь!'})

    # Для отображения в шаблоне нам нужен объект слова, если мы еще не показали фидбек
    display_word = None
    if not feedback and current_word_id:
        display_word = Word.objects.get(id=current_word_id)

    return render(request, 'learning/quiz.html', {
        'form': form,
        'word': display_word,
        'feedback': feedback,
        'correct_answer': correct_answer,
        'score': request.session['score']
    })

def reset_score(request):
    """
    reset score
    """
    request.session['score'] = 0
    return redirect('quiz_view')
