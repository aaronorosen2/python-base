# Generated by Django 3.1.4 on 2020-12-30 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses_api', '0018_auto_20201229_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersessionevent',
            name='user_session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses_api.usersession'),
        ),
    ]