# Generated by Django 4.0.6 on 2023-02-19 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0031_remove_comments_service'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='description',
        ),
    ]
