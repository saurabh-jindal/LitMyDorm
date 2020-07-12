from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('category/<str:slug>', views.category, name='category'),
    path('add_to_cart/<str:slug>', views.add_to_cart, name='add_to_cart'),
    path('view_product/<str:slug>', views.view_product, name='view_product'),
    path('order_summary/', views.order_summary, name='order_summary'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<str:payment_option>', views.payment, name='payment'),
    path('signup/', views.handleSignup, name="handleSignup"),
    path('login/', views.handleLogin, name="handleLogin"),
    path('logout/', views.handleLogout, name="handleLogout"),
]


