# Generated by Django 5.1.2 on 2024-10-24 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mess_app', '0014_hostelbillsettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expenditure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expenditure_date', models.DateField()),
                ('expenditure_type', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bill_image', models.ImageField(upload_to='bills/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
