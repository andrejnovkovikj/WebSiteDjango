# Generated by Django 4.2.4 on 2023-08-14 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_item_sex_item_type'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Item',
            new_name='Product',
        ),
    ]
