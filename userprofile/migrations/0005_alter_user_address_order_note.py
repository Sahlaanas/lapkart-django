# Generated by Django 4.2.1 on 2023-06-01 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_user_address_order_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_address',
            name='order_note',
            field=models.TextField(max_length=300),
        ),
    ]
