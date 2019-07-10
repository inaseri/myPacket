from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addtransactions/', views.addTransaction, name='addTransactions'),
    path('addbank/', views.addBank, name='addBank'),
    path('banks/', views.banks, name='banks')
]