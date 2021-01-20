# Generated by Django 3.1.4 on 2020-12-29 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses_api', '0012_auto_20201222_1626'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=256)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='flashcardresponse',
            name='user',
        ),
        migrations.AddField(
            model_name='flashcardresponse',
            name='signature',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='flashcardresponse',
            name='user_session',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='courses_api.usersession'),
            preserve_default=False,
        ),
    ]