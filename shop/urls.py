from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import categories, subcategories, products

urlpatterns = [
    path('', views.index, name="index"),
    path('products/', views.products, name='products'),
    path('products/<int:product_id>/', views.product, name='product'),

    path('signup/', views.signup, name='signup'),
    # path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:product_id>/', views.increase_cart, name='increase_cart'),
    path('cart/decrease/<int:product_id>/', views.decrease_cart, name='decrease_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('categories/', categories, name='categories'),
    path('categories/<int:category_id>/', subcategories, name='subcategories'),
    path('categories/<int:category_id>/products/', products, name='products'),


]  # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)