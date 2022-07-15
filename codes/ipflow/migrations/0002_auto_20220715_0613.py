# Generated by Django 3.1.4 on 2022-07-15 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipflow', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flowlog',
            name='created_at',
        ),
        migrations.AddField(
            model_name='flowlog',
            name='account_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='flowlog',
            name='dstaddr',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='flowlog',
            name='dstport',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='flowlog',
            name='interface_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='flowlog',
            name='protocol',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='flowlog',
            name='srcaddr',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='flowlog',
            name='srcport',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
