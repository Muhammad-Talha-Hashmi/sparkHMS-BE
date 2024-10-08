# Generated by Django 5.0.6 on 2024-08-12 11:26

import utils.methods
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(blank=True, null=True)),
                ('status', models.PositiveSmallIntegerField(blank=True, default=2, null=True)),
                ('name', models.TextField()),
                ('address', models.TextField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, default='assets/no_image.png', null=True, upload_to='assets/')),
                ('display_name', models.TextField(blank=True, null=True)),
                ('domain', models.CharField(blank=True, null=True)),
                ('contact_no', models.CharField(blank=True, max_length=16, null=True)),
                ('contact_email', models.CharField(blank=True, max_length=30, null=True)),
                ('website', models.CharField(blank=True, max_length=60, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HotelInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=255)),
                ('quantity', models.PositiveIntegerField()),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InventoryRestock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restock_date', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.PositiveIntegerField()),
                ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_cost', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(blank=True, null=True)),
                ('status', models.PositiveSmallIntegerField(blank=True, default=2, null=True)),
                ('name', models.TextField()),
                ('address', models.TextField(blank=True, null=True)),
                ('org_key', models.TextField(default=utils.methods.organization_key_generator)),
                ('logo', models.ImageField(blank=True, default='assets/no_image.png', null=True, upload_to='assets/')),
                ('display_name', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'organization',
            },
        ),
    ]
