from django.contrib import admin
from .models import (
    Profile, Vendor, Category, Image, Product, ProductVariant,
    Order, OrderItem, Payment, Review, Discount, Wishlist,
    Notification, Analytics
)

# 1. Profile
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_vendor', 'phone_number', 'address', 'created_at']
admin.site.register(Profile, ProfileAdmin)

# 2. Vendor
class VendorAdmin(admin.ModelAdmin):
    list_display = ['user', 'store_name', 'subscription_plan', 'subscription_expiry', 'created_at', 'updated_at']
admin.site.register(Vendor, VendorAdmin)

# 3. Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
admin.site.register(Category, CategoryAdmin)

# 4. Image
class ImageAdmin(admin.ModelAdmin):
    list_display = ['image_name']
admin.site.register(Image, ImageAdmin)

# 5. Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor', 'price', 'category', 'created_at', 'updated_at']
admin.site.register(Product, ProductAdmin)

# 6. ProductVariant
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'value', 'pricemodifier', 'stock']
admin.site.register(ProductVariant, ProductVariantAdmin)

# 7. Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'order_date', 'status', 'total_amount']
admin.site.register(Order, OrderAdmin)

# 8. OrderItem
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_variant', 'quantity', 'price']
admin.site.register(OrderItem, OrderItemAdmin)

# 9. Payment
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'payment_method', 'payment_status']
admin.site.register(Payment, PaymentAdmin)

# 10. Review
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
admin.site.register(Review, ReviewAdmin)

# 11. Discount
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'value', 'start_date', 'end_date', 'is_active', 'vendor']
admin.site.register(Discount, DiscountAdmin)

# 12. Wishlist
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at', 'added_at']
admin.site.register(Wishlist, WishlistAdmin)

# 13. Notification
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'is_read', 'created_at']
admin.site.register(Notification, NotificationAdmin)

# 14. Analytics
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'total_sales', 'total_orders', 'total_customers', 'total_visitors', 'total_revenue', 'date']
admin.site.register(Analytics, AnalyticsAdmin)
