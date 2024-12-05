from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.movie_form, name='movie_form'),
    path('list/', views.movie_list, name='movie_list'),
    path('upload/', views.upload_json, name='upload_json'),
]
