from django import forms
from .models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'genre', 'year']

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year < 1900 or year > 2100:
            raise forms.ValidationError("Год должен быть в пределах от 1900 до 2100.")
        return year
