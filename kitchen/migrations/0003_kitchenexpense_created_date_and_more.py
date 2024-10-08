# Generated by Django 5.0.6 on 2024-09-10 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0002_kitchenfinancialstatement_kitchen'),
    ]

    operations = [
        migrations.AddField(
            model_name='kitchenexpense',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default="2024-09-30"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='kitchenrevenue',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default="2024-09-30"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='kitchenexpense',
            name='date',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='kitchenrevenue',
            name='date',
            field=models.CharField(max_length=50),
        ),
    ]
