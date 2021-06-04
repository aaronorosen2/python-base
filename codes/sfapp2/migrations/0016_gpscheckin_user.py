# Generated by Django 2.2.8 on 2021-05-28 06:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sfapp2', '0015_videoupload_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='gpscheckin',
            name='user',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]