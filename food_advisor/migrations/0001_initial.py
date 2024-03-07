# Generated by Django 2.2.28 on 2024-03-07 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=128)),
                ('timeOpens', models.TimeField(default='12:00:00')),
                ('timeCloses', models.TimeField(default='12:00:00')),
                ('tags', models.CharField(blank=True, max_length=128)),
                ('cuisineType', models.CharField(blank=True, max_length=128)),
                ('name', models.CharField(max_length=128)),
                ('starRating', models.IntegerField(blank=True, choices=[(0, '0 stars'), (1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')])),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regDate', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(max_length=128, unique=True)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1280)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('replyContent', models.CharField(max_length=128)),
                ('starRating', models.IntegerField(choices=[(0, '0 stars'), (1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')])),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_advisor.Restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_advisor.User')),
            ],
        ),
        migrations.AddField(
            model_name='restaurant',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_advisor.User'),
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
