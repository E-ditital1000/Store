from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('payment/', views.payment, name='payment'),
]
