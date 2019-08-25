from django.contrib import admin
from .models import Banks,Transactions,User,AbstractUser

admin.site.register(Banks)
admin.site.register(Transactions)
admin.site.register(User)
# Register your models here.
