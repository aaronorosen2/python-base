# Generated by Django 3.1.4 on 2021-02-26 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('neighbormade', '0001_initial'),
        ('store', '0013_auto_20210226_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='Neighborhood',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='neighbormade.neighborhood'),
        ),
    ]
