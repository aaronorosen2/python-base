# Generated by Django 3.1.4 on 2022-08-08 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vconf', '0015_auto_20220622_1632'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='roominfo',
            table='roominfo',
        ),
        migrations.AlterModelTable(
            name='roomrecording',
            table='roomrecording',
        ),
        migrations.AlterModelTable(
            name='roomvisitors',
            table='roomvisitors',
        ),
    ]
