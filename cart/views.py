from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
import uuid
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from store.models import Product, Variation

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
    product_variations= []
    cart = get_or_create_cart(request)
    
    if request.method == "POST" :
        for key, value in request.POST.items() :
            print(key + value)
            try :
                variation = Variation.objects.get(product= product,variation_category__iexact= key, variation_value= value)
                
                product_variations.append(variation)
                
            except Variation.DoesNotExist :
                continue  
    if request.user.is_authenticated :
        cart_items = CartItem.objects.filter(user= request.user, product = product)  
    else :      
        cart_items = CartItem.objects.filter(product = product , cart = cart)
        
    for cart_item in cart_items :
        existing_variations= list(cart_item.variations.all())
        if existing_variations == product_variations :
            cart_item.quantity += 1
            cart_item.save()
            return redirect("cart:cart")
        
    if request.user.is_authenticated :
        cart_item = CartItem.objects.create(user= request.user, product= product)
    else :
        cart_item = CartItem.objects.create(cart = cart, product= product)
        
    cart_item.variations.set(product_variations)
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
    if request.user.is_authenticated :
        cart_items = CartItem.objects.filter(user= request.user, is_active= True)
    else :
        cart = get_or_create_cart(request)
        cart_items = CartItem.objects.filter(cart= cart, is_active= True)
        
    total = sum(item.sub_total() for item in cart_items)
    tax = (2*total)//100
    context = {"total": total, "cart_items": cart_items, "tax": tax}
    return render(request, "store/cart.html", context)


@login_required(login_url= "account:login")
def checkout(request) :
    if request.user.is_authenticated :
        cart_items = CartItem.objects.filter(user= request.user, is_active= True)
    else :
        cart = get_or_create_cart(request)
        cart_items = CartItem.objects.filter(cart= cart, is_active= True)
    total = sum(item.sub_total() for item in cart_items)
    tax = (2*total)//100
    context = {"total": total, "cart_items": cart_items, "tax": tax}
    return render(request, "store/checkout.html", context)