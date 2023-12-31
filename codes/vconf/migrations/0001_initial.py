# Generated by Django 3.1.4 on 2021-02-09 09:43

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo_img_url', models.CharField(max_length=500)),
                ('room_name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='RoomInfo',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=50, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('room_name', models.CharField(max_length=50, unique=True)),
                ('logo_url', models.TextField()),
                ('video_url', models.CharField(default='', max_length=500)),
                ('slack_channel', models.CharField(max_length=500, unique=True)),
            ],
            options={
                'db_table': 'roominfo',
            },
        ),
        migrations.CreateModel(
            name='Vistor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=2000)),
                ('email', models.EmailField(blank=True, max_length=512, null=True)),
                ('phone', models.CharField(blank=True, max_length=24, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoomVisitors',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=50, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vconf.roominfo')),
            ],
            options={
                'db_table': 'roomvisitors',
            },
        ),
        migrations.CreateModel(
            name='RoomRecording',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=50, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('recording_link', models.TextField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vconf.roominfo')),
            ],
            options={
                'db_table': 'roomrecording',
            },
        ),
    ]
