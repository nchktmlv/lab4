from django.db import models

# Create your models here.

from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()

    def __str__(self):
        return self.title

# # Импорт модуля models из библиотеки Django
# from django.db import models
# # Определение класса MyModel, который наследует модель Django Model
# class MyModel(models.Model):
#     # Определение поля id типа AutoField как первичного ключа
#     id = models.AutoField(primary_key=True)
#     # Определение поля phone типа CharField с максимальной длиной в 20 символов
#     phone = models.CharField(max_length=20)

#     # Определение метода __str__, который будет использоваться для представления экземпляров модели в виде строки
#     def __str__(self):
#         return self.phone