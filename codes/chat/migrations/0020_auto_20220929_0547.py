# Generated by Django 3.1.4 on 2022-09-29 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0019_auto_20220928_0829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='isExist',
            field=models.CharField(choices=[('0', 'exist'), ('5', 'arcade')], default='0', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='channelmember',
            name='designation',
            field=models.CharField(choices=[('0', 'joined'), ('1', 'cancel'), ('2', 'leave'), ('3', 'requested'), ('4', 'terminated'), ('5', 'arcade')], default='0', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userrequest',
            name='request_type',
            field=models.CharField(choices=[('0', 'joined'), ('1', 'cancel'), ('2', 'leave'), ('3', 'requested'), ('4', 'terminated'), ('5', 'arcade')], default='3', max_length=256),
        ),
    ]