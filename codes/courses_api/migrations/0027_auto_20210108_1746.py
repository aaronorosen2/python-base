# Generated by Django 3.1.4 on 2021-01-08 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_api', '0026_remove_flashcardresponse_signature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashcardresponse',
            name='answer',
            field=models.TextField(),
        ),
    ]
