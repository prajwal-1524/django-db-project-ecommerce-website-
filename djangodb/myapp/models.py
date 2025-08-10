from django.db import models
from django.contrib.auth.models import User 
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    #user table xa django sim and yo profile ra user ko one to one relationship banaye maile
    #models.cascade vaneko if on_delete of user , tyo user sanga related profile pani delete gardinu vaneko ho 
    
    is_vendor = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Vendor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='vendor')    
    # one user has one vendor
    # relate_name : it is used to fetch user information from vendor and vendor information from user
    store_name = models.CharField(max_length=50)
    description = models.TextField(blank=True,null=True)
                                #blank for frontend ,null for backend
    logo = models.ImageField(upload_to='vendor_logos/',blank=True,null=True )  
    subscription_plan = models.CharField(max_length=50,choices=[('basic','Basic'),('premium','Premium'),('enterprise','Enterprise')],default='basic')
    subscription_expiry = models.DateTimeField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.store_name

class Category(models.Model):
    name =  models.CharField(max_length=50)
    slug = models.SlugField(unique=True)       
    parent = models.ForeignKey('self', on_delete=models.CASCADE,blank=True, null=True,related_name='children')
                            #self : denotes self referencing, category ko ni sub category hos vanne chahera
                            # The parent field tells:
                            # "Which category is the parent of this category?"
                            # parent object is pointing to another object similar to itself
                            # related_name='children' yo rakhyo vaney child name bata related parent lai tanna sakxu using reverser query
    class Meta:
        verbose_name_plural = 'Categories'  #admin pannel ma table ko yei name dekhauna ko lagi 

   
    def __str__(self):
        return self.name
                            

class Image(models.Model):

    image_name = models.ImageField(upload_to='product_image', height_field=None, width_field=None, max_length=None)
    # images xuttai folder ma upload hunxa
    # upload_to vaneko image upload huney folder ko naam ho
    # xuttai class banako ho so that we can use this image in product model
    def __str__(self):
        return self.image_name.url if self.image_name else 'No Image Found'

class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,related_name='products')
    # vendor le product add garne ho so as a foreign key vendor lai product ma rakhya ho
    # on_delete=models.CASCADE vaneko vendor delete bhayo vaney tyo vendor sanga
    # related products pani delete huncha
    # related_name='products' vaneko vendor ko products lai tanna sakos vanera
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,related_name='products')
    product_image = models.ForeignKey(Image, on_delete=models.CASCADE,related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
                            
class ProductVariant(models.Model): #like shoes product ma size, color, etc. haru huna sakxa
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100) #size, color, etc.
    value = models.CharField(max_length=100) #L, M, S, Red, Blue, etc.
    pricemodifier = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.name}: {self.value} ({self.product.name})"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.CharField(max_length=255)
    shipping_method = models.CharField(max_length=50)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
        
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product_variant.name} ({self.order.id})"        

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    # related_name='payments' allows us to access payments related to an order
    payment_method = models.CharField(max_length=50, choices=[('khalti','Khalti'), ('ime pay','IME Pay'), ('cod','Cash on Delivery')], default='khalti')
    # choices includes databse values and human readable values ,tuples kept inside list because tuples are immutable the databasevalues and human readable values are not going to change, and list preserves the order since frontend ma payment method haru ko lai order ma dekhauna parcha
    payment_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.payment_method} ({self.payment_status})"
        # "Payment for Order 101 - Khalti (Success)"
        # 🔹 self.order.id

        # self refers to the current object (e.g., a Payment).

        # self.order is a related Order object.

        # .id is the ID (primary key) of that order.

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username} - Rating: {self.rating}"

class Discount(models.Model):
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    discount_type = models.CharField(max_length=20, choices=[('percentage', 'Percentage'), ('fixed', 'Fixed Amount')], default='percentage')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    minimum_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_limit = models.PositiveIntegerField(default=1)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='discounts', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.code

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)
    added_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Wishlist - {self.product.name}" 

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message[:20]}..."  # Display first 20 characters of the message               

class Analytics(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='analytics')
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_orders = models.PositiveIntegerField(default=0)
    total_customers = models.PositiveIntegerField(default=0)
    total_visitors = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    date= models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Analytics for {self.vendor.store_name} - Total Sales: {self.total_sales}"
