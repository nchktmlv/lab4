import json
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import Movie
from .forms import MovieForm
from django import forms
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
# from .models import UserData


# Путь к директории с файлами JSON
JSON_DIR = os.path.join(settings.BASE_DIR, 'movies_json')


def save_movie_to_json(movie):
    if not os.path.exists(JSON_DIR):
        os.makedirs(JSON_DIR)

    # Создаем словарь с необходимыми данными
    movie_dict = {
        'title': movie.title,
        'genre': movie.genre,
        'year': movie.year,
    }

    # Имя файла будет основано на названии фильма
    filename = os.path.join(JSON_DIR, f"{movie.title.replace(' ', '_')}.json")
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(movie_dict, json_file, ensure_ascii=False, indent=4)


def movie_form(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save()
            save_movie_to_json(movie)
            return redirect('movie_list')
    else:
        form = MovieForm()

    return render(request, 'movies/movie_form.html', {'form': form})


def movie_list(request):
    source = request.GET.get('source')  # Нет значения по умолчанию, чтобы избежать автоматического выбора
    if not source:
        source = 'db'  # Если параметр не передан, то установим 'db' как источник данных по умолчанию.

    query = request.GET.get('query', '')  # Получаем строку для поиска
    data = []

    if source == 'db':
        # Получение данных из базы данных с фильтрацией
        movies = Movie.objects.all()
        if query:
            movies = movies.filter(title__icontains=query)  # Фильтрация по названию
        data = [{"id": movie.id, "title": movie.title, "genre": movie.genre, "year": movie.year} for movie in movies]
    elif source == 'json':
        # Получение данных из JSON-файлов с фильтрацией
        if os.path.exists(JSON_DIR):
            for filename in os.listdir(JSON_DIR):
                if filename.endswith('.json'):
                    file_path = os.path.join(JSON_DIR, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as json_file:
                            json_data = json.load(json_file)
                            if query.lower() in json_data.get('title', '').lower():  # Поиск по названию
                                data.append(json_data)
                    except json.JSONDecodeError:
                        continue  # Пропускаем некорректные файлы

    return render(request, 'movies/movie_list.html', {'data': data, 'source': source})






def upload_json(request):
    if request.method == 'POST' and request.FILES.get('json_file'):
        json_file = request.FILES['json_file']

        # Проверка на тип файла
        if not json_file.name.endswith('.json'):
            return render(request, 'movies/upload_json.html', {'error': 'Только файлы JSON разрешены.'})

        try:
            data = json.load(json_file)
            # Пример валидации данных
            if 'title' not in data or 'genre' not in data or 'year' not in data:
                raise ValidationError("Некорректные данные в файле. (файл не содержит 'title', 'genre' и 'year'")

        except (json.JSONDecodeError, ValidationError) as e:
            return render(request, 'movies/upload_json.html', {'error': f'Ошибка в файле: {e}'})

        # Сохранение в файл (путь к файлу использует json_file.name)
        file_path = os.path.join(JSON_DIR, json_file.name)
        with open(file_path, 'wb') as destination:
            for chunk in json_file.chunks():
                destination.write(chunk)

        return redirect('movie_list')

    return render(request, 'movies/upload_json.html')


class StorageChoiceForm(forms.Form):
    STORAGE_CHOICES = [
        ('json', 'JSON'),
        ('db', 'Database'),
    ]
    storage = forms.ChoiceField(choices=STORAGE_CHOICES, widget=forms.RadioSelect)

def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        save_to = request.POST.get('save_to')  # Получаем выбор пользователя (json или db)

        if form.is_valid() and save_to:
            movie_data = form.cleaned_data  # Извлекаем данные из формы

            if save_to == 'db':  # Сохранение в базу данных
                # Проверка на дубликаты по названию
                if Movie.objects.filter(title=movie_data['title']).exists():
                    messages.error(request, 'Фильм с таким названием уже существует в базе данных!')
                else:
                    form.save()  # Сохраняем только в базу данных
                    messages.success(request, 'Фильм успешно сохранён в базу данных!')

            elif save_to == 'json':  # Сохранение в JSON
                save_movie_to_json(form.instance)  # Сохранение данных в JSON
                messages.success(request, 'Фильм успешно сохранён в JSON-файл!')

            return redirect('movie_list')

        else:
            messages.error(request, 'Ошибка в форме! Убедитесь, что все поля заполнены и выбран способ сохранения.')

    else:
        form = MovieForm()

    return render(request, 'movies/movie_form.html', {'form': form})



def load_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_movies(request):
    source = request.GET.get('source', 'db')  # Значение по умолчанию - 'db'

    if source == 'db':
        movies = Movie.objects.all()
    elif source == 'json':
        movies = load_from_json()
    else:
        movies = []

    return render(request, 'movies/list_movies.html', {'movies': movies, 'source': source})


def ajax_search(request):
    query = request.GET.get('query', '')

    # Фильтрация данных по базе данных
    results = Movie.objects.filter(title__icontains=query)  # Фильтрация по названию
    data = [{"title": movie.title, "genre": movie.genre, "year": movie.year} for movie in results]

    # Возвращаем JSON-ответ
    return JsonResponse(data, safe=False)

def edit_record(request, record_id):
    movie = get_object_or_404(Movie, id=record_id) #получаем объект фильма из базы данных по его идентификатору. Если фильм с таким идентификатором не найден, будет возвращена ошибка 404.

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Фильм успешно отредактирован!')
            return redirect('movie_list')
        else:
            messages.error(request, 'Ошибка при редактировании фильма.')
    else:
        form = MovieForm(instance=movie)

    return render(request, 'movies/edit_movie.html', {'form': form, 'movie': movie})



def delete_record(request, record_id):
    movie = get_object_or_404(Movie, id=record_id)

    if request.method == "POST":
        movie.delete()
        messages.success(request, 'Фильм успешно удален!')
        return redirect('movie_list')

    return redirect('movie_list')





# Код для запуска сервера
# python manage.py runserver

# http://127.0.0.1:8000/movies/add/
