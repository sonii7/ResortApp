# Generated by Django 5.1.1 on 2024-10-15 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_remove_reservation_dinner_remove_reservation_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='is_available',
        ),
        migrations.RemoveField(
            model_name='room',
            name='price_per_night',
        ),
        migrations.AddField(
            model_name='room',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('Occupied', 'Occupied')], default='unknown', max_length=20),
            preserve_default=False,
        ),
    ]