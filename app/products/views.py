# views.py
from django.shortcuts import render
from django.db.models import Q
from .models import Product

def product_list(request):
    query = request.GET.get('q', '')  # Get the search query from the URL parameters
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(title__icontains=query) | Q(brand__name__icontains=query)
        )

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'products/product_listing.html', context)
