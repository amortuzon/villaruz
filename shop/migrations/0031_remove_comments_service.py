# Generated by Django 4.0.6 on 2023-02-19 04:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0030_alter_comments_service'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='service',
        ),
    ]
