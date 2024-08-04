# Generated by Django 5.0.6 on 2024-08-04 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='staffTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, max_length=120)),
                ('name', models.CharField(blank=True, max_length=60)),
                ('contact', models.CharField(blank=True, max_length=60)),
                ('emergency_contact', models.CharField(blank=True, max_length=120)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('nationlaity', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('responsibilities', models.CharField(blank=True, max_length=120)),
            ],
        ),
    ]
