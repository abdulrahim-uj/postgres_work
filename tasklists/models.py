from django.db import models
from versatileimagefield.fields import VersatileImageField

from basics.models import BaseModel


class Task(BaseModel):
    name = models.CharField(max_length=128)
    priority = models.IntegerField()
    status = models.IntegerField()

    def __str__(self):
        return self.name
