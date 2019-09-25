from django.urls import path,include
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.homePage, name='index'),
    path('accounts/login/', views.clogin, name='login'),
    path(r'accounts/logout/',views.clogout,name="logout"),
    url('addtransactions/(?P<type>[0-9])/', views.addTransaction, name='addTransactions'),
    url('addbank/(?P<type>[0-9]){1,3}/', views.addBank, name='addBank'),
    url('banks/(?P<type>[0-9]){1,3}', views.banks, name='banks'),
    path('register/', views.register, name='register'),
    path('home/',views.homePage, name='home'),
    url(r'transactions/(?P<type>[0-9])/',views.index, name='transactions'),
]

