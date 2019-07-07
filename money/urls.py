from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.addTransaction, name='addTransactions'),
    path('accounts/', include('django.contrib.auth.urls'))
]