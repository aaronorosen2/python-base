# Generated by Django 3.1.4 on 2021-03-18 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voip', '0019_auto_20210318_0455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_leads',
            name='status',
            field=models.CharField(choices=[('-', '-'), ('Call back later', 'Call back later'), ('not interested', 'not interested')], default='-', max_length=20),
        ),
    ]