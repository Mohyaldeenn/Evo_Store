from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.

class CustomUserAdmin(UserAdmin) :
    model = UserAdmin
    list_display = ("full_name", "email", "is_staff", "last_login", "date_joined", "is_active",)
    list_filter = ("is_staff", "is_active",)
    search_fields = ("email", "full_name",)
    ordering = ("-date_joined",)
    readonly_fields = ("last_login", "date_joined",)
    fieldsets = ()
    
admin.site.register(CustomUser, CustomUserAdmin)