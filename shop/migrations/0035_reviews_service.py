# Generated by Django 4.1.7 on 2023-02-24 02:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0034_alter_shop_date_alter_shop_time_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.service'),
        ),
    ]
