# Generated by Django 5.0.6 on 2024-06-04 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_customer_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_no',
            field=models.CharField(max_length=220),
        ),
    ]
