# Generated by Django 2.2 on 2024-03-19 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_advisor', '0008_alter_cuisinetype_id_alter_userprofile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuisinetype',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
