from django.shortcuts import render

# Create your views here.
import json
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import Movie
from .forms import MovieForm

# Путь к директории с файлами JSON
JSON_DIR = os.path.join(settings.BASE_DIR, 'movies_json')


def save_movie_to_json(movie):
    if not os.path.exists(JSON_DIR):
        os.makedirs(JSON_DIR)

    movie_data = {
        'title': movie.title,
        'genre': movie.genre,
        'year': movie.year,
    }

    # Имя файла будет основано на названии фильма
    filename = os.path.join(JSON_DIR, f"{movie.title.replace(' ', '_')}.json")

    with open(filename, 'w') as json_file:
        json.dump(movie_data, json_file)


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
    movies = Movie.objects.all()
    json_files = []

    if os.path.exists(JSON_DIR):
        for filename in os.listdir(JSON_DIR):
            if filename.endswith('.json'):
                with open(os.path.join(JSON_DIR, filename), 'r') as json_file:
                    json_data = json.load(json_file)
                    json_files.append(json_data)

    return render(request, 'movies/movie_list.html', {'movies': movies, 'json_files': json_files})


from django.core.exceptions import ValidationError


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

        # Сохранение в файл
        with open(os.path.join(JSON_DIR, json_file.name), 'wb') as destination:
            for chunk in json_file.chunks():
                destination.write(chunk)

        return redirect('movie_list')

    return render(request, 'movies/upload_json.html')

# Код для запуска сервера
# python manage.py runserver

# http://127.0.0.1:8000/movies/add/

