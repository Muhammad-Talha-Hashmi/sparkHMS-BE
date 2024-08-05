# Generated by Django 5.0.6 on 2024-08-05 17:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('house_keeping', '0002_initial'),
        ('rooms', '0001_initial'),
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='housekeeping',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='housekeeping_schedule', to='rooms.room'),
        ),
        migrations.AddField(
            model_name='housekeeping',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='staff.stafftable'),
        ),
    ]
