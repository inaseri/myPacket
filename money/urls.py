from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.homePage, name='index'),
    path('accounts/login/', views.clogin, name='login'),
    path(r'accounts/logout/',views.clogout,name="logout"),
    path('addtransactions/', views.addTransaction, name='addTransactions'),
    path('addbank/', views.addBank, name='addBank'),
    path('banks/', views.banks, name='banks'),
    path('register/', views.register, name='register'),
    path('home/',views.homePage, name='home'),
    path('transactions/',views.index, name='transactions'),
]

