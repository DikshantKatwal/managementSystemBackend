# Generated by Django 5.1.3 on 2024-12-19 07:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_alter_employee_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='start_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]