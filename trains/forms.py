from django import forms

from cities.models import City
from trains.models import Train


class HtmlForm(forms.Form):
    name = forms.CharField(label='Номер поезда')


class TrainForm(forms.ModelForm):
    name = forms.CharField(label='Номер поезда', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите номер поезда'}))

    travel_time = forms.IntegerField(label='Время в пути', widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Укажите время в пути'}))

    from_city = forms.ModelChoiceField(label='Город отправления',
                                       queryset=City.objects.all(),
                                       widget=forms.Select(attrs={
                                           'class': 'form-control'}
                                       ))

    to_city = forms.ModelChoiceField(label='Город прибытия',
                                     queryset=City.objects.all(),
                                     widget=forms.Select(attrs={
                                         'class': 'form-control'}
                                     ))

    class Meta:
        model = Train
        fields = '__all__'
