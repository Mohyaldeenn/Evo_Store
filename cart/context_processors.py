from .models import CartItem
from .views import get_or_create_cart

def counter(request) :
    if request.user.is_authenticated :
        cart_items = CartItem.objects.filter(user= request.user).count()
    else :
        cart = get_or_create_cart(request)
        cart_items = CartItem.objects.filter(cart= cart).count()
    return {"cart_count" : cart_items}
    