# Generated by Django 5.1.2 on 2024-10-24 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mess_app', '0015_expenditure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenditure',
            name='expenditure_type',
            field=models.CharField(choices=[('grocery', 'Grocery'), ('food', 'Food'), ('utility', 'Utility'), ('maintenance', 'Maintenance'), ('salary', 'Staff Salary'), ('miscellaneous', 'Miscellaneous')], max_length=20),
        ),
    ]
