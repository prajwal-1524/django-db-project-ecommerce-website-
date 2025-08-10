from django.shortcuts import render
from .models import Product
# Create your views here.
def homepage(request):
    products = Product.objects.all()  # Fetch all products from the database

    context = {
        'products':products  # Pass the products to the template
    }
    return render(request, 'index.html', context=context)
