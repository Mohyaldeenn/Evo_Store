from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model) :
    name = models.CharField( max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="photos/categories/", blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    def get_absolute_url(self):
        return reverse("store:product_by_category", kwargs={"category_slug": self.slug})