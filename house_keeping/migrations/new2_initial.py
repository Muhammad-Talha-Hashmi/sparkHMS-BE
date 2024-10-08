# Generated by Django 5.0.6 on 2024-08-13 12:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('house_keeping', 'new1_initial'),
        ('rooms', 'new1_initial')
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
