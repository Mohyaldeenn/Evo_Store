from django.db import models
from django.urls import reverse
from category.models import Category

# Create your models here.
class Product (models.Model) :
    name = models.CharField( max_length=200, unique=True, blank= False, null= False)
    slug = models.SlugField(max_length=250, unique= True)
    description = models.CharField( max_length=254, blank= True)
    price = models.IntegerField()
    image = models.ImageField( upload_to="photos/products")
    stock = models.IntegerField()
    is_available = models.BooleanField(default= True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField( auto_now_add=True)
    modified_date = models.DateTimeField( auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('store:product_detail', kwargs={'category_slug': self.category.slug, "product_slug": self.slug})