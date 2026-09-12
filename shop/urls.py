from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/get/', views.get_cart, name='get_cart'),
]