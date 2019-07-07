from django.db import models

class Banks(models.Model):
    name_bank = models.CharField(max_length=100)
    cash_bank = models.IntegerField(default=0)

    def __str__(self):
        return self.name_bank


class Transactions(models.Model):
    source = models.ForeignKey(Banks,on_delete=models.CASCADE)
    date = models.DateTimeField()
    title = models.CharField(max_length=100)
    cash = models.IntegerField(default=0)
    desc = models.TextField()
    type = models.IntegerField(default=1)

    def __str__(self):
        return self.title