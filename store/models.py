from django.db import models
from category.models import Category
from django.urls import reverse

class Product(models.Model):
    product_name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products/')
    stock  = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.product_name
    
    def get_product_url(self):
        return reverse('store:product_detail', args=[self.category.slug, self.slug])
   