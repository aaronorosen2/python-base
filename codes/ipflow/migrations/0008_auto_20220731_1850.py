# Generated by Django 3.1.4 on 2022-07-31 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipflow', '0007_auto_20220731_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flowlog',
            name='bytes_size',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
