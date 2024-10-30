# Generated by Django 5.1.2 on 2024-10-16 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mess_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='birth_date',
            new_name='dob',
        ),
        migrations.RenameField(
            model_name='customuser',
            old_name='phone_number',
            new_name='ph_no',
        ),
        migrations.AddField(
            model_name='customuser',
            name='course',
            field=models.CharField(blank=True, choices=[('CS', 'Computer Science'), ('IT', 'Information Technology'), ('ENG', 'Engineering'), ('BIZ', 'Business'), ('ART', 'Arts')], max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='end_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='guard_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='guard_phn',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='reg_no',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='sem',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='start_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
