# Generated by Django 5.1.2 on 2024-10-20 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_hostelbilldetail_student'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Student',
        ),
    ]
