from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('products/<int:product_id>/', views.product, name='product'),

    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
]