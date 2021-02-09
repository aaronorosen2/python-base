# Generated by Django 3.1.4 on 2021-02-09 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_api', '0031_invite'),
    ]

    operations = [
        migrations.AddField(
            model_name='invite',
            name='invite_type',
            field=models.CharField(choices=[(0, 'none'), (1, 'email'), (2, 'text')], default=0, max_length=1),
        ),
    ]
