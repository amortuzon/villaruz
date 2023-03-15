from django.db import models
from django.contrib.auth.models import User

import re
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import time
# regex to validate phone numbers
phone_regex = re.compile(
    r'^\+?1?\d{9,15}$'
)


class Customer(models.Model):
    phone_regex = RegexValidator(
        regex=phone_regex,
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True, null=True, unique=False)
    email = models.EmailField(max_length=200, blank=True, null=True)
    profile_pic = models.ImageField(
        default="profile.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Shop(models.Model):
    COMPLETE = (
        ('New', 'New'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed'),
    )
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=200, null=True, choices=COMPLETE, default='New')
    service = models.ManyToManyField(Service)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True, validators=[
                            MinValueValidator(time(9, 0)), MaxValueValidator(time(17, 0))])
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.name

    class Meta:
        ordering = ['-created']


class Comments(models.Model):
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.CASCADE)
    # service = models.ForeignKey(
    #     Service, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    message = models.TextField(null=True, blank=False)
    rating = models.FloatField()
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message


class Reviews(models.Model):
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, null=True, on_delete=models.CASCADE)
    review = models.TextField(null=True, blank=False)
    rating = models.FloatField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review
