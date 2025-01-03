from .models import Cart, CartItem
from .views import _get_cart_id

def counter(request) :
    cart = Cart.objects.get(cart_id = _get_cart_id(request))
    cart_item = CartItem.objects.filter(cart= cart).count()
    return {"cart_count" : cart_item}