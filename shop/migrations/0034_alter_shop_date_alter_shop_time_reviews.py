# Generated by Django 4.0.6 on 2023-02-20 07:49

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0033_remove_shop_service_shop_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='time',
            field=models.TimeField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(datetime.time(9, 0)), django.core.validators.MaxValueValidator(datetime.time(17, 0))]),
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(null=True)),
                ('rating', models.FloatField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.customer')),
            ],
        ),
    ]
