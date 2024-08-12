# Generated by Django 5.0.6 on 2024-08-12 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(blank=True, null=True)),
                ('status', models.PositiveSmallIntegerField(blank=True, default=2, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.CharField(choices=[('Inventory', 'Inventory'), ('Salary', 'Salary'), ('Maintenance', 'Maintenance'), ('Utilities', 'Utilities'), ('Other', 'Other')], max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HotelFinancialStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(blank=True, null=True)),
                ('status', models.PositiveSmallIntegerField(blank=True, default=2, null=True)),
                ('period_start', models.DateField()),
                ('period_end', models.DateField()),
                ('total_expenses', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total_revenues', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('net_profit', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Revenue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(blank=True, null=True)),
                ('status', models.PositiveSmallIntegerField(blank=True, default=2, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.CharField(choices=[('Room Booking', 'Room Booking'), ('Food & Beverage', 'Food & Beverage'), ('Service', 'Service'), ('Other', 'Other')], max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
