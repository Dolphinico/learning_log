from django.conf.urls import url
# Сначала импортируется представление login по умолчанию:
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from . import views

"""Определяет схемы URL для пользователей"""
app_name = 'users'

urlpatterns = [
    # Страница входа
    # Когда Django читает этот URL-адрес, слово users указывает, что следует обратиться к users/urls.py,
    # а login сообщает о том, что запросы должны отправляться представлению login по умолчанию
    url(r'^login/$', LoginView.as_view(), name='login'),

]