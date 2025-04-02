# learning/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Word
from .forms import WordForm, ExportForm
from reportlab.pdfgen import canvas  # Для PDF


# 1. Список слов
def word_list(request):
    words = Word.objects.all()
    return render(request, 'learning/word_list.html', {'words': words})


# 2. Детальная страница
def word_detail(request, pk):
    word = get_object_or_404(Word, pk=pk)
    return render(request, 'learning/word_detail.html', {'word': word})


# 3. Форма 1: Создание слова
def word_create(request):
    if request.method == "POST":
        form = WordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('word_list')
    else:
        form = WordForm()
    return render(request, 'learning/word_form.html', {'form': form, 'title': 'Добавить новое слово'})


# 4. Форма 2: Экспорт в PDF
def export_pdf(request):
    if request.method == "POST":
        form = ExportForm(request.POST)
        if form.is_valid():
            difficulty = form.cleaned_data['difficulty']
            include_examples = form.cleaned_data['include_examples']

            # Фильтрация данных
            if difficulty == 'all':
                words = Word.objects.all()
            else:
                words = Word.objects.filter(difficulty=difficulty)

            # Генерация PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="vocabulary_{difficulty}.pdf"'

            p = canvas.Canvas(response)
            p.setFont("Helvetica", 16)
            p.drawString(100, 800, f"Vocabulary List: {difficulty}")

            y = 750
            p.setFont("Helvetica", 12)
            for word in words:
                p.drawString(100, y, f"{word.english_word} - {word.translation}")
                if include_examples and word.example_sentence:
                    y -= 15
                    p.drawString(120, y, f"Example: {word.example_sentence}")
                y -= 25
                if y < 50:  # Переход на новую страницу, если место кончилось
                    p.showPage()
                    y = 800

            p.showPage()
            p.save()
            return response
    else:
        form = ExportForm()

    return render(request, 'learning/export_form.html', {'form': form})