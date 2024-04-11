from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from category.models import Category
from . models import Product


def store(request, category_slug= None):
    categories = None
    products = None
    # try:
    #     categories = Category.objects.get(slug=category_slug)
    # except Category.DoesNotExist:
    #     return HttpResponse(f'Category with {category_slug} does not exist!!!')
    if category_slug != None:
        # Using Try ana except
        categories =get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=categories,is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()
        
        
    context = {
        "products": products,
        "product_count": product_count
    }
    return render(request, 'store/store.html',context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e:
        raise e
    context = {
        "single_product": single_product
    }
    return render(request, 'store/product_detail.html', context)