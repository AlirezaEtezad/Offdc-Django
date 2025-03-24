from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Customer(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
        # return super().__str__()

    ...


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey(
        'self',  # Self-referencing for subcategories
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='subcategories'
    )

    def __str__(self):
        return self.name if not self.parent else f'{self.parent.name} > {self.name}'



class Product(models.Model):

    brand = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=15, decimal_places=0)
    description = models.TextField()
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
  #  image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"Image for {self.product.name}"

class Comment:
    ...

class Rate:
    ...
    

class Cart(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE) # each user has one cart
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} * {self.product.name}'
    
class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=15, decimal_places=0)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'



    
