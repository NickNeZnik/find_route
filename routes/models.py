from django.db import models

from cities.models import City


class Route(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название маршрута')

    total_travel_time = models.PositiveSmallIntegerField(verbose_name='Общее время в пути')

    from_city = models.ForeignKey(City, on_delete=models.CASCADE,
                                  related_name='route_from_city_set',
                                  verbose_name='Город отправления')
    to_city = models.ForeignKey('cities.City', on_delete=models.CASCADE,
                                related_name='route_to_city_set',
                                verbose_name='Город прибытия')
    trains = models.ManyToManyField('trains.Train', verbose_name='Список поездов')


    def __str__(self):
        return f'Маршрут {self.name} из {self.from_city} в {self.to_city}'

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
        ordering = ['total_travel_time']
