# Generated by Django 5.1.2 on 2024-10-20 07:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mess_app', '0012_employee_joined_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeleave',
            name='added_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
