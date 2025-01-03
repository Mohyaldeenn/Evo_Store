from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.view_cart, name="cart"),
    path("add_to_cart/<int:product_id>/", views.add_to_cart, name= "add_to_cart"),
    path("remove_from_cart/<int:item_id>/", views.remove_from_cart, name= "remove_from_cart"),
    path("decrement_quantity/<int:item_id>/", views.decrement_quantity, name= "decrement_quantity"),
]
