# Generated by Django 3.1.7 on 2021-04-07 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voip', '0030_auto_20210402_0542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calllist',
            name='date',
            field=models.DateField(),
        ),
    ]