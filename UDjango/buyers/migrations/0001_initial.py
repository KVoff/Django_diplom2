# Generated by Django 5.1.2 on 2024-11-10 08:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=255)),
                ('house_number', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('special_notes', models.TextField(blank=True, null=True)),
                ('phone_number', models.CharField(max_length=12, unique=True, validators=[django.core.validators.RegexValidator(message='Введите корректный номер телефона (например, +79991234567).', regex='^\\+7\\d{10}$')])),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('addresses', models.ManyToManyField(blank=True, related_name='buyers', to='buyers.address')),
                ('groups', models.ManyToManyField(blank=True, related_name='buyer_set', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='buyer_permissions', to='auth.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
