# Generated by Django 5.1.2 on 2024-10-20 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mess_app', '0010_employee_leave'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Leave',
            new_name='EmployeeLeave',
        ),
        migrations.AddField(
            model_name='employee',
            name='ph_no',
            field=models.CharField(max_length=15, null=True),
        ),
    ]