from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from cart.views import _get_cart_id
from cart.models import Cart, CartItem
#########
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
##########
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .forms import RegistrationForm
from .models import CustomUser
# Create your views here.

def dashboard(request):
    return render(request, "account/dashboard.html")

def register(request) :
    if request.method== "POST" :
        form = RegistrationForm(request.POST)
        if form.is_valid() :
            email = form.cleaned_data["email"]
            user = CustomUser.objects.create_user(
                full_name = form.cleaned_data["full_name"],
                email = email,
                password = form.cleaned_data["password"]
            )
            user.save()
            #########
            mail_subject = "please activate your account"
            user = user
            domain = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            message = render_to_string('account/activation_mail.html', {
                "user": user, "domain": domain, "uid": uid, "token": token
                })
            send_mail(mail_subject, message, from_email="me@gmail.com" ,recipient_list=[email,])
            
            #########
            messages.success(request, "go to your mail to valid your account")
            return redirect("account:register")
    else :
        form = RegistrationForm()
    context = {"form" :form}
    return render(request, "account/register.html", context)


def login(request) :
    if request.method == "POST" :
        email = request.POST["email"]
        password = request.POST["password"]
        next_url = request.POST.get('next', "")
        if not next_url : next_url= reverse("store:home")
        user = auth.authenticate(email= email, password= password)
        if user is not None :
            cart = Cart.objects.get(cart_id= _get_cart_id(request))
            cart_item_exists = CartItem.objects.filter(cart= cart).exists()
            if cart_item_exists :
                cart_item = CartItem.objects.filter(cart= cart)
                for item in cart_item :
                    item.user = user
                    item.save()      
            auth.login(request, user)
            messages.success(request, "You Are Login in now")
            return redirect(next_url)
        else :
            messages.error(request, "Invalid Login Credentials")
            return redirect("account:login")
    return render(request, "account/login.html",)


@login_required(login_url= "account:login")
def logout(request) :
    auth.logout(request)
    return redirect("account:login")

def activate(request, uidb64, token) :
    try :
        uid = force_str( urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(id= uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist ) :
        user = None
    if user is not None and default_token_generator.check_token(user, token) :
        user.is_active = True
        user.save()
        messages.success(request, "your account has been activated successfully")
        return redirect("account:login")
    else :
        return HttpResponse("Link is not valid")
    
    
def forgotPassword(request):
    if request.method == "POST" :
        email = request.POST["email"]
        if CustomUser.objects.filter(email= email).exists() :
            user = CustomUser.objects.get(email__exact= email)
            #########
            
            mail_subject = "reset your password"
            user = user
            domain = get_current_site(request).domain
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            message = render_to_string('account/reset_password_mail.html', {
                "user": user, "domain": domain, "uid": uid, "token": token
                })
            send_mail(mail_subject, message, from_email="me@gmail.com" ,recipient_list=[email,])
            messages.success(request, "password reset email has been sent to your email address")
            return redirect("account:login")
            #########
        else :
            messages.error(request, "account with this email does not exist")
            return redirect("account:forgotPassword")
    return render(request, "account/forgotPassword.html")


def resetPasswordValidate(request, uidb64, token):
    try :
        uid = force_str( urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(id= uid)
        if not default_token_generator.check_token(user, token) :
            return HttpResponse("Link is invalid or has been expired")
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist ) :
        user = None
    if user is not None and default_token_generator.check_token(user, token) :
        return render(request, "account/reset_password.html", {"uid" : uidb64, "token": token})
    else :
        messages.error(request, "Link is invalid or has been expired")
        return redirect("account:forgotPassword")


def setPassword(request, uidb64, token): 
    if request.method == "POST" :
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        
        try :
            uid = force_str( urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id= uid)
            if not default_token_generator.check_token(user, token) :
                messages.error(request, "Link is not invalid or has been expired")
                return redirect("account:forgotPassword")
            if password != confirm_password :
                messages.error(request, "passwords does not match")
                return redirect(request.path)
            try :
                validate_password(password, user)
            except ValidationError as e :
                messages.error(request, e)
                return redirect(request.path)
            
            user.password = make_password(password)
            user.save()
            messages.success(request, "password has been reset successfully")
            return redirect("account:login")
        
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist ) :
            messages.error(request, "error happened. please try again")
            return redirect("account:forgotPassword")
    
    return render(request, "account/reset_password.html", {"uid": uidb64, "token": token})
        
    
           