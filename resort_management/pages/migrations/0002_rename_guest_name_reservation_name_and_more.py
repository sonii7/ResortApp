# Generated by Django 5.1.1 on 2024-10-04 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='guest_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='status',
        ),
        migrations.AddField(
            model_name='reservation',
            name='dinner',
            field=models.CharField(default='None', max_length=50),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='room_type',
            field=models.CharField(choices=[('standard', 'Standard'), ('deluxe', 'Deluxe'), ('suite', 'Suite')], max_length=10),
        ),
    ]
