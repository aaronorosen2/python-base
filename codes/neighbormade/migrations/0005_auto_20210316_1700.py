# Generated by Django 3.1.4 on 2021-03-16 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neighbormade', '0004_reddit'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Reddit',
            new_name='Subreddit',
        ),
    ]
