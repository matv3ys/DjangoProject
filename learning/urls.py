from django.urls import path
from . import views

urlpatterns = [
    path('', views.word_list, name='word_list'),
    path('word/<int:pk>/', views.word_detail, name='word_detail'),
    path('word/add/', views.word_create, name='word_create'),
    path('export/', views.export_pdf, name='export_pdf'),
]