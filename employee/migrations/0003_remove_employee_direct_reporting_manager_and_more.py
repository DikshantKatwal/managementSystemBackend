# Generated by Django 5.1.3 on 2024-12-18 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_alter_employee_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='direct_reporting_manager',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='emergency_contact_prefix',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='postal_code',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='start_date',
        ),
    ]