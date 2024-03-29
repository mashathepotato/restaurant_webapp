# Generated by Django 2.2.28 on 2024-03-07 14:16

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
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=128)),
                ('timeOpens', models.TimeField(default='12:00:00')),
                ('timeCloses', models.TimeField(default='12:00:00')),
                ('tags', models.CharField(blank=True, max_length=128, null=True)),
                ('cuisineType', models.CharField(blank=True, max_length=128, null=True)),
                ('name', models.CharField(max_length=128)),
                ('starRating', models.DecimalField(decimal_places=4, default=0, max_digits=10)),
                ('totalReviews', models.IntegerField(default=0)),
                ('manager', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=1280)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('replyContent', models.CharField(default='', max_length=128)),
                ('starRating', models.IntegerField(choices=[(0, '0 stars'), (1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')], default=0)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_advisor.Restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('price', models.IntegerField()),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_advisor.Restaurant')),
            ],
            options={
                'verbose_name_plural': 'Dishes',
            },
        ),
    ]
