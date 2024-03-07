# Generated by Django 2.2.28 on 2024-03-07 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_advisor', '0003_auto_20240307_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='starRating',
            field=models.IntegerField(choices=[(0, '0 stars'), (1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')], default=0),
        ),
    ]