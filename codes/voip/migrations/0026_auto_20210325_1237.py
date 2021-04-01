# Generated by Django 3.1.4 on 2021-03-25 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voip', '0025_auto_20210325_1036'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='user_leads',
            name='uniqueUserLead',
        ),
        migrations.AddConstraint(
            model_name='user_leads',
            constraint=models.UniqueConstraint(fields=('name', 'phone', 'email', 'price', 'state', 'url', 'notes', 'status', 'last_call', 'recording_url'), name='uniqueUserLead'),
        ),
    ]
