# Generated by Django 2.2.8 on 2020-11-11 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sfapp2', '0010_videoupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoupload',
            name='video_uuid',
            field=models.CharField(default='', max_length=500),
        ),
    ]
