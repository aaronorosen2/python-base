# Generated by Django 3.1.4 on 2022-10-03 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0024_auto_20221003_0704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlastseen',
            name='last_visit',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]