# Generated by Django 4.2.1 on 2023-05-30 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_remove_user_address_house_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_address',
            name='address',
            field=models.TextField(default='Address', max_length=300),
        ),
    ]
