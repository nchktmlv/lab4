# Импорт модуля admin из библиотеки Django.contrib
from django.contrib import admin
# Импорт модели MyModel из текущего каталога (".")
# from .models import MyModel
# # Регистрация модели MyModel для административного сайта
# admin.site.register(MyModel)

from django.contrib import admin
from .models import Movie

admin.site.register(Movie)


