# Generated by Django 4.1.5 on 2023-01-11 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0013_remove_message_rating"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="rating",
            field=models.IntegerField(
                choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=3
            ),
        ),
    ]
