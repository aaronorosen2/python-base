# Generated by Django 2.2.8 on 2021-05-11 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_api', '0049_auto_20210504_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashcardresponse',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='flashcardresponse',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]