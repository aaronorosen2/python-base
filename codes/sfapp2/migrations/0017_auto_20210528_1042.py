# Generated by Django 2.2.8 on 2021-05-28 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sfapp2', '0016_gpscheckin_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpscheckin',
            name='member',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='sfapp2.Member'),
        ),
        migrations.AlterField(
            model_name='videoupload',
            name='member',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='sfapp2.Member'),
        ),
    ]
