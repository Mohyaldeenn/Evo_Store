from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from cart.models import CartItem
from .forms import OrderForm
from .models import Order

# Create your views here.
def place_order(request):
    current_user = request.user
    cart_items = CartItem.objects.filter(user= current_user, is_active= True)
    total = sum(item.sub_total() for item in cart_items)
    tax = (2*total)//100
    cart_count = cart_items.count()
    if cart_count <= 0 :
        return redirect("store:store")
    if request.method == "POST" :
        form = OrderForm(request.POST)
        if form.is_valid() :
            data = Order()
            data.full_name = form.cleaned_data["full_name"]
            data.phone = form.cleaned_data["phone"]
            data.email = form.cleaned_data["email"]
            data.address_line_1 = form.cleaned_data["address_line_1"]
            data.address_line_2 = form.cleaned_data["address_line_2"]
            data.phone = form.cleaned_data["phone"]
            data.state = form.cleaned_data["state"]
            data.city = form.cleaned_data["city"]
            data.order_note = form.cleaned_data["order_note"]
            data.order_total = total
            data.tax = tax
            data.user = current_user
            data.ip = request.META.get('REMOTE_ADDR')
            
            data.save()
            order_id = datetime.today().strftime('%y%m%d') + str(data.id)
            data.order_number = order_id
            data.save()

            return HttpResponse(data)
        if not form.is_valid():
            print(form.errors)
    return redirect("cart:checkout")

