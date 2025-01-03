from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product
from category.models import Category
from cart.models import CartItem
from cart.views import _get_cart_id
# Create your views here.

def home(request) :
    products = Product.objects.filter(is_available=True)
    context = { "products" :products}
    return render(request, "home.html", context )


def store(request, category_slug= None) :
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True).order_by('id')
    
    if category_slug :
        category = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category = category).order_by('id')
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page') 
    page_products = paginator.get_page(page_number)
    
    context = { "products" :page_products, "categories": categories, "products_count": products.count()}
    return render(request, "store/store.html", context)


def product_detail(request, category_slug= None, product_slug= None) :
    product = get_object_or_404(Product, category__slug = category_slug, slug= product_slug)
    in_cart = CartItem.objects.filter(cart__cart_id=_get_cart_id(request), product= product).exists()
    context = {"product" : product, "in_cart": in_cart}
    return render(request,"store/product_detail.html", context)