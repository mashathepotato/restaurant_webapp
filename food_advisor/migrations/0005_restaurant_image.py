# Generated by Django 4.2.11 on 2024-03-08 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_advisor', '0004_auto_20240307_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='image',
            field=models.ImageField(blank=True, upload_to='restaurant_images'),
        ),
    ]
