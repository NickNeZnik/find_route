# Generated by Django 4.0.2 on 2022-02-17 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trains', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='train',
            options={'ordering': ['name'], 'verbose_name': 'Поезд', 'verbose_name_plural': 'Поезда'},
        ),
    ]