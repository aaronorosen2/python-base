# Generated by Django 2.2.8 on 2020-12-12 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_order_braintreeid'),
    ]

    operations = [
        migrations.CreateModel(
            name='subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('braintreeSubscriptionID', models.CharField(blank=True, max_length=70, null=True)),
                ('first_name', models.CharField(max_length=70)),
                ('last_name', models.CharField(blank=True, max_length=70)),
                ('Company_name', models.CharField(max_length=70)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(blank=True, default='', max_length=200)),
                ('address', models.CharField(blank=True, max_length=128)),
                ('city', models.CharField(blank=True, max_length=70)),
                ('state', models.CharField(blank=True, max_length=70)),
                ('postal_code', models.IntegerField(blank=True)),
                ('is_ordered', models.BooleanField(default=False)),
                ('date_ordered', models.DateTimeField(auto_now=True)),
                ('plan_ID', models.CharField(max_length=70)),
            ],
        ),
    ]
