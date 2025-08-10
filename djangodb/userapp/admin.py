from django.contrib import admin
from .models import CustomUser  # Import the CustomUser model we created

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone_number']
admin.site.register(CustomUser, CustomUserAdmin)
