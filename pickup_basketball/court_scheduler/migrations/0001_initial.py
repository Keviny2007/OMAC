# Generated by Django 5.1.1 on 2024-09-26 05:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('court_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('signed_up_at', models.DateTimeField(auto_now_add=True)),
                ('time_slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='court_scheduler.timeslot')),
            ],
        ),
    ]
