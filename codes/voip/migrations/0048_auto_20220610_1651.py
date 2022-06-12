# Generated by Django 3.1.4 on 2022-06-10 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voip', '0047_auto_20220610_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.CharField(blank=True, max_length=34, null=True, unique=True)),
                ('date', models.DateTimeField()),
                ('from_number', models.CharField(max_length=20, null=True)),
                ('to_number', models.CharField(max_length=20, null=True)),
                ('recording_url', models.CharField(max_length=500, null=True)),
                ('duration', models.CharField(max_length=10, null=True)),
                ('direction', models.CharField(max_length=30, null=True)),
            ],
            options={
                'db_table': 'CallList',
            },
        ),
        migrations.DeleteModel(
            name='CallList',
        ),
    ]