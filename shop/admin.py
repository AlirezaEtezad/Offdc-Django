from django.contrib import admin
from .models import Customer, Cart, CartItem, Order, OrderItem, Product, ProductImage, Category

# ✅ Register Customer and Cart
admin.site.register(Customer)

# ✅ Inline for displaying Cart Items inside Cart
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    fields = ['product', 'quantity']
    autocomplete_fields = ['product']

# ✅ Cart Admin (Includes Cart Items)
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username']
    inlines = [CartItemInline]  # Show items inside cart

# ✅ Inline for displaying Order Items inside Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ['product', 'quantity']
    autocomplete_fields = ['product']

# ✅ Order Admin Configuration
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'total_price']
    list_filter = ['created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'total_price']
    inlines = [OrderItemInline]  # Show items inside order



# ✅ Product Image Inline for Admin Panel
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

# ✅ Product Admin Configuration
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ['brand', 'name', 'price', 'stock', 'category']
    list_filter = ['category', 'brand']
    search_fields = ['name', 'brand', 'category']
    list_editable = ['price']

# ✅ Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
