# Generated by Django 3.1.4 on 2021-02-24 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voip', '0007_call_loist'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Call_loist',
            new_name='Call_list',
        ),
    ]
