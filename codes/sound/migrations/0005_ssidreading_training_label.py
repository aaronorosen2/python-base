# Generated by Django 3.1.4 on 2022-08-02 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wifi', '0004_auto_20220615_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='ssidreading',
            name='training_label',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]
