# Generated by Django 5.1.2 on 2024-10-17 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mess_app', '0006_alter_customuser_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='guard_phn',
            field=models.CharField(max_length=15, null=True),
        ),
    ]