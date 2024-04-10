from django.db import models


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