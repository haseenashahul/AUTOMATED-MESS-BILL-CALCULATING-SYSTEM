# Generated by Django 5.1.2 on 2024-10-20 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_hostelbilldetail_broadband_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostelbilldetail',
            name='total',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
