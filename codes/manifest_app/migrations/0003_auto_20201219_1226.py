# Generated by Django 2.2.8 on 2020-12-19 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manifest_app', '0002_auto_20201218_1909'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='description',
        ),
        migrations.RemoveField(
            model_name='event',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='event',
            name='start_time',
        ),
        migrations.RemoveField(
            model_name='event',
            name='title',
        ),
        migrations.AddField(
            model_name='event',
            name='email',
            field=models.EmailField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='event',
            name='name',
            field=models.CharField(default='', max_length=70),
        ),
        migrations.AddField(
            model_name='event',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
