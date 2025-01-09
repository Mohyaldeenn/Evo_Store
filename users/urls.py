from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name= "register"),
    path("login/", views.login, name= "login" ),
    path("logout/", views.logout, name= "logout"), 
    path("forgotPassword/", views.forgotPassword, name= "forgotPassword"),
    path("activate/<str:uidb64>/<str:token>/", views.activate, name= "activate"), 
    path("resetPasswordValidate/<str:uidb64>/<str:token>/", views.resetPasswordValidate, name= "resetPasswordValidate"),
    path("setPassword/<str:uidb64>/<str:token>/", views.setPassword, name= "setPassword"),
]
