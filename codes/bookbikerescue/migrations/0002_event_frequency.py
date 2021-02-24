from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookbikerescue', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='frequency',
            field=models.CharField(blank=True, choices=[('0', 'None'), ('bg-primary', 'Daily'), ('bg-success', 'Weekly'), ('bg-danger', 'Biweekly')], default='0', max_length=224, null=True),
        ),
    ]
