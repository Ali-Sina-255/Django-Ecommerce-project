from django.db import models
from django.urls import reverse
class Category(models.Model):
    category_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    cart_image = models.ImageField(upload_to='photos/category/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
    
    def __str__(self) -> str:
        return self.category_name
    
    def get_category_url(self):
        return reverse("store:product_by_category",args=[self.slug])