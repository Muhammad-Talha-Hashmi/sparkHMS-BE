# Generated by Django 5.0.6 on 2024-08-05 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amenities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(blank=True, null=True)),
                ('status', models.PositiveSmallIntegerField(blank=True, default=2, null=True)),
                ('invoice_number', models.CharField(max_length=20, unique=True)),
                ('invoice_date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_paid', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(blank=True, null=True)),
                ('status', models.PositiveSmallIntegerField(blank=True, default=2, null=True)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('is_paid', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(blank=True, null=True)),
                ('status', models.PositiveSmallIntegerField(blank=True, default=2, null=True)),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(blank=True, null=True)),
                ('status', models.PositiveSmallIntegerField(blank=True, default=2, null=True)),
                ('Name', models.CharField(blank=True, max_length=120, null=True)),
                ('room_type', models.CharField(blank=True, max_length=60, null=True)),
                ('bed_type', models.CharField(blank=True, max_length=60, null=True)),
                ('price', models.CharField(blank=True, max_length=120, null=True)),
                ('availability', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('notes', models.CharField(blank=True, max_length=120, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RoomBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(blank=True, null=True)),
                ('status', models.PositiveSmallIntegerField(blank=True, default=2, null=True)),
                ('guest_name', models.CharField(max_length=255)),
                ('guest_email', models.EmailField(max_length=254)),
                ('guest_phone', models.CharField(max_length=20)),
                ('check_in', models.DateTimeField()),
                ('check_out', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
