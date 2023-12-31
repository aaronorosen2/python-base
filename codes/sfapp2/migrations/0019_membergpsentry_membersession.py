# Generated by Django 3.1.4 on 2021-06-02 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sfapp2', '0018_auto_20210602_1201'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('ended_at', models.DateTimeField()),
                ('member', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='sfapp2.member')),
            ],
        ),
        migrations.CreateModel(
            name='MemberGpsEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('device_timestamp', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('member_session', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='sfapp2.membersession')),
            ],
        ),
    ]
