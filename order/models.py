from django.db import models
from users.models import CustomUser
from store.models import Product, Variation

# Create your models here.

class Payment(models.Model) :
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_id = models.CharField( max_length=100)
    payment_method = models.CharField( max_length=100)
    amount_paid = models.FloatField()
    status = models.CharField( max_length=100)
    created_at = models.DateTimeField( auto_now_add=True)
    
    def __str__(self):
        return self.payment_id
    

class Order(models.Model) :
    STATUS = (
        ('New', 'New'), ('Accepted','Accepted'), ('Completed','Completed'), ('Cancelled','Cancelled'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=100)
    full_name = models.CharField( max_length=200)
    email = models.CharField( max_length=100)
    phone = models.CharField( max_length=15, null= True)
    address_line_1 = models.CharField( max_length=100)
    address_line_2 = models.CharField( max_length=100, blank=True)
    state = models.CharField( max_length=100)
    city = models.CharField( max_length=100)
    order_note = models.CharField( max_length=250)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField( max_length=15, choices=STATUS, default="New")
    ip = models.GenericIPAddressField( protocol="both", blank=True , null= True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)

    def __str__(self):
        return self.full_name
    
    
class OrderProduct(models.Model) :
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    color = models.CharField( max_length=50)
    size = models.CharField( max_length=50)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)
    
    def __str__(self):
        return self.product.name