# Generated by Django 4.2.4 on 2023-08-20 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_rename_username_client_address_remove_client_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='expirationDate',
            field=models.CharField(max_length=10),
        ),
    ]
