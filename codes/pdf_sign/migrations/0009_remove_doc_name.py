# Generated by Django 2.2.8 on 2020-12-09 05:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_sign', '0008_auto_20201209_1104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doc',
            name='name',
        ),
    ]