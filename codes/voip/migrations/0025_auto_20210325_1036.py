# Generated by Django 3.1.4 on 2021-03-25 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voip', '0024_auto_20210324_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_leads',
            name='status',
            field=models.CharField(default='-', max_length=20),
        ),
        migrations.AddConstraint(
            model_name='user_leads',
            constraint=models.UniqueConstraint(fields=('name', 'phone', 'email', 'price', 'state', 'url', 'notes'), name='uniqueUserLead'),
        ),
        migrations.AlterModelTable(
            name='user_leads',
            table='User_leads',
        ),
    ]