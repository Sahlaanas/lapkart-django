# Generated by Django 4.2.1 on 2023-06-01 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_alter_user_address_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_address',
            name='order_note',
            field=models.TextField(default=None, max_length=300),
        ),
    ]
