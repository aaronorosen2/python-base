# Generated by Django 2.2.8 on 2020-10-26 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sfapp2', '0004_auto_20201025_0509'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='population_list',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='services_list',
            field=models.TextField(blank=True, null=True),
        ),
    ]