from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass


class Banks(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name_bank = models.CharField(max_length=100)
    cash_bank = models.IntegerField(default=0)

    def __str__(self):
        return self.name_bank


class Transactions(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.ForeignKey(Banks,on_delete=models.CASCADE)
    date = models.DateTimeField()
    title = models.CharField(max_length=100)
    cash = models.IntegerField(default=0)
    desc = models.TextField(default="بدون توضیحات")
    type = models.IntegerField()

    def __str__(self):
        return self.title
