# Generated by Django 5.1.4 on 2024-12-18 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_movie_genre_alter_movie_title_alter_movie_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
