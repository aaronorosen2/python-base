# Generated by Django 3.1.4 on 2021-03-02 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stadium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('capacity', models.IntegerField()),
                ('city', models.CharField(max_length=250)),
                ('state', models.CharField(blank=True, max_length=250, null=True)),
                ('country', models.CharField(max_length=250)),
                ('region', models.CharField(max_length=250)),
                ('teams', models.CharField(max_length=250)),
                ('sports', models.CharField(max_length=250)),
                ('image', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('frequency', models.CharField(blank=True, choices=[('0', 'None'), ('bg-primary', 'Daily'), ('bg-success', 'Weekly'), ('bg-danger', 'Biweekly')], default='0', max_length=224, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('stadium', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bookingstadium.stadium')),
            ],
        ),
    ]