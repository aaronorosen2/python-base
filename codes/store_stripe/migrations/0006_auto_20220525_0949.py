# Generated by Django 3.1.4 on 2022-05-25 04:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses_api', '0063_flashcard_stripe_config'),
        ('store_stripe', '0005_stripedetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='email',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='is_complete',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='stripe_intent_id',
        ),
        migrations.AddField(
            model_name='transaction',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='lesson',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses_api.lesson'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='stripe_session_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]