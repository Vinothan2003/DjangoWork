# Generated by Django 5.0.6 on 2024-06-03 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='first_name',
            new_name='given_name',
        ),
    ]
