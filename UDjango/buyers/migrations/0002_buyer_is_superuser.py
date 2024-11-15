# Generated by Django 5.1.2 on 2024-11-11 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
    ]
