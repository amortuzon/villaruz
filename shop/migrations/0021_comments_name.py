# Generated by Django 4.1.5 on 2023-01-21 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_rename_name_comments_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]