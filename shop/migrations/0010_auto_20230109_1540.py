# Generated by Django 3.1.6 on 2023-01-09 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='name',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.customer'),
        ),
    ]
