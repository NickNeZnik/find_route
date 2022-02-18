from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from cities.models import City


class Train(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Номер поезда')
    travel_time = models.PositiveSmallIntegerField(verbose_name='Время в пути')
    from_city = models.ForeignKey(City, on_delete=models.CASCADE,
                                  related_name='from_city_set',
                                  verbose_name='Город отправления')
    to_city = models.ForeignKey('cities.City', on_delete=models.CASCADE,
                                related_name='to_city_set',
                                verbose_name='Город прибытия')

    def __str__(self):
        return f'Поезд {self.name} из {self.from_city} в {self.to_city}'

    class Meta:
        verbose_name = 'Поезд'
        verbose_name_plural = 'Поезда'
        ordering = ['name']

    def clean(self):
        if self.from_city == self.to_city:
            raise ValidationError('Город отправления и город прибытия не могут совпадать!')
        qs = Train.objects.filter(from_city=self.from_city,
                                  to_city=self.to_city,
                                  travel_time=self.travel_time).exclude(pk=self.pk)
        # Train == self.__class__
        if qs.exists():
            raise ValidationError('Запись с подобными полями уже существует')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)



# def get_absolute_url(self):
#     return reverse('cities:detail', kwargs={'pk': self.pk})
