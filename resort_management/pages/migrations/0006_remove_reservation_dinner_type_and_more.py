# Generated by Django 5.1.1 on 2024-10-16 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_remove_room_is_available_remove_room_price_per_night_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='dinner_type',
        ),
        migrations.AddField(
            model_name='reservation',
            name='dinner_preference',
            field=models.CharField(default='unknown', max_length=50),
            preserve_default=False,
        ),
    ]
