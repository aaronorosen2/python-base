# Generated by Django 2.2.8 on 2020-12-05 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_sign', '0005_auto_20201205_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doc',
            name='comments',
            field=models.TextField(default=''),
        ),
    ]