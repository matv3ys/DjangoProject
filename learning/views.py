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
