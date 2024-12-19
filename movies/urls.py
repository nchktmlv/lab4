from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_movie, name='add_movie'),
    path('list/', views.movie_list, name='movie_list'),
    path('upload/', views.upload_json, name='upload_json'),
    path('list/ajax_search/', views.ajax_search, name='ajax_search'),
    path('edit/<int:record_id>/', views.edit_record, name='edit_record'),
    path('delete/<int:record_id>/', views.delete_record, name='delete_record'),
]

