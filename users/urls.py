from django.urls import path
# Сначала импортируется представление login по умолчанию:
from django.contrib.auth.views import LoginView
from . import views

"""Определяет схемы URL для пользователей"""
app_name = 'users'

urlpatterns = [
    # Страница входа
    # Когда Django читает этот URL-адрес, слово users указывает, что следует обратиться к users/urls.py,
    # а login сообщает о том, что запросы должны отправляться представлению login по умолчанию
    # страница входа:
    path('login/', LoginView.as_view(template_name = 'users/login.html'),name='login'),
    # страница выхода:
    path('logout/', views.logout_view, name='logout'),
    # страница регистрации
    path('register/', views.register, name='register'),
]