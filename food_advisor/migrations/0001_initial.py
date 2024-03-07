# Generated by Django 2.2.28 on 2024-03-06 16:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=128)),
                ('timeOpens', models.TimeField()),
                ('timeCloses', models.TimeField()),
                ('url', models.URLField()),
                ('tags', models.CharField(max_length=128)),
                ('cuisineType', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=128)),
                ('avg_stars', models.DecimalField(decimal_places=4, max_digits=10)),
                ('total_ratings', models.IntegerField()),
                ('manager', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Restaurants',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1280)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('replyContent', models.CharField(max_length=1280)),
                ('starRating', models.IntegerField()),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_advisor.Restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Reviews',
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('price', models.IntegerField()),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_advisor.Restaurant')),
            ],
            options={
                'verbose_name_plural': 'Dishes',
            },
        ),
    ]
