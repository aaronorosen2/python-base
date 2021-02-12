# Generated by Django 3.1.4 on 2021-02-11 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SMS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=20, null=True)),
                ('msg', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('twilio_phone', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='voip.phone')),
            ],
        ),
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('time_duration', models.IntegerField(default=0)),
                ('twilio_phone', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='voip.phone')),
            ],
        ),
    ]