# Generated by Django 5.1.4 on 2024-12-18 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.PositiveIntegerField(),
        ),
    ]