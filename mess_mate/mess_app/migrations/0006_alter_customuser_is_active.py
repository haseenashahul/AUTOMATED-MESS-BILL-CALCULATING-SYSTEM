# Generated by Django 5.1.2 on 2024-10-17 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mess_app', '0005_alter_customuser_address_alter_customuser_course_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
