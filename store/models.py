from django.db import models
from django.urls import reverse
from category.models import Category

# Create your models here.
class VariationManager(models.Manager) :
    def colors(self) :
        return super(VariationManager, self).filter(variation_category = "color", is_active= True)
    def sizes(self) :
        return super(VariationManager, self).filter(variation_category = "size", is_active= True)
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
  
  
class Variation(models.Model) :
    variation_category_choice = (("color", "color"), ("size", "size"))
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField( max_length=100, choices= variation_category_choice )  
    variation_value = models.CharField( max_length=100)
    is_active = models.BooleanField(default= True)
    created_date = models.DateTimeField( auto_now_add=True)
    objects = VariationManager()
    def __str__(self):
        return self.variation_value
      
    