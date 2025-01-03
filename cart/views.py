from django.shortcuts import render, get_object_or_404, redirect
import uuid
from .models import Cart, CartItem
from store.models import Product

# Create your views here.

def _get_cart_id(request) :
    cart_id = request.session.get('cart_id')
    if not cart_id :
        cart_id = str(uuid.uuid4())
        request.session['cart_id'] = cart_id
    return cart_id

def get_or_create_cart(request) :
    cart_id = _get_cart_id(request)
    cart, create = Cart.objects.get_or_create(cart_id= cart_id)
    return cart 

def add_to_cart(request, product_id) :
    product = get_object_or_404(Product, id = product_id)
    cart = get_or_create_cart(request)
    cart_item, create = CartItem.objects.get_or_create(product = product , cart = cart)
    if not create :
        cart_item.quantity += 1
    cart_item.save()
    return redirect("cart:cart")

def remove_from_cart(request, item_id) :
    cart_item = CartItem.objects.get(id= item_id)
    cart_item.delete()
    return redirect("cart:cart")

def decrement_quantity(request, item_id) :
    cart_item = CartItem.objects.get(id= item_id)
    if cart_item.quantity > 1 :
        cart_item.quantity -= 1
        cart_item.save()
    return redirect("cart:cart")

def view_cart(request) :
    cart = get_or_create_cart(request)
    cart_items = CartItem.objects.filter(cart= cart, is_active= True)
    total = sum(item.sub_total() for item in cart_items)
    tax = (2*total)//100
    context = {"total": total, "cart_items": cart_items, "tax": tax}
    return render(request, "store/cart.html", context)