# Generated by Django 3.1.4 on 2021-05-20 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FaceSwap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/image')),
                ('video', models.FileField(blank=True, null=True, upload_to='media/video')),
                ('result', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='UploadImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_image', models.ImageField(blank=True, null=True, upload_to='uploadimg/')),
            ],
        ),
    ]
