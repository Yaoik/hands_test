# Generated by Django 5.1.7 on 2025-06-04 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='operation_id',
            field=models.UUIDField(primary_key=True, serialize=False, verbose_name='ID операции'),
        ),
    ]
