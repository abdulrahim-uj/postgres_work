from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class phonetest(models.Model):
    name = models.TextField()
    # An optional phone number.
    phone_number = PhoneNumberField(blank=True)
