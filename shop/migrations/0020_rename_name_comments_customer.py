# Generated by Django 4.1.5 on 2023-01-21 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_rename_message_comments'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='name',
            new_name='customer',
        ),
    ]