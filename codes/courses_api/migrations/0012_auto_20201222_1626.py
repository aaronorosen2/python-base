# Generated by Django 3.1.4 on 2020-12-22 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses_api', '0011_flashcardresponse'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flashcardresponse',
            old_name='FlashCard',
            new_name='flashcard',
        ),
    ]