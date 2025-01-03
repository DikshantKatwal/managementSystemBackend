# Generated by Django 5.1.3 on 2024-12-24 05:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0004_checkinhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkin',
            name='check_out',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='checkin',
            name='check_out_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='checkin',
            name='check_out_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='checkin',
            name='total_days',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='checkin',
            name='total_paid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('restored_at', models.DateTimeField(blank=True, null=True)),
                ('transaction_id', models.UUIDField(blank=True, null=True)),
                ('agreed_price', models.IntegerField(blank=True, null=True)),
                ('amount_paid', models.IntegerField(blank=True, null=True)),
                ('remaining', models.IntegerField(blank=True, null=True)),
                ('payment_on', models.DateTimeField(auto_now_add=True)),
                ('checkin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='checkin_payments', to='room.checkin')),
            ],
            options={
                'db_table': 'payments',
            },
        ),
    ]
