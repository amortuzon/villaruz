# Generated by Django 4.1.5 on 2023-01-21 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_remove_message_user_alter_message_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Message',
            new_name='Comments',
        ),
    ]
