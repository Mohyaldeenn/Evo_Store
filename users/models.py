from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.

class CustomUserManager(BaseUserManager) :
    def create_user(self, full_name, email, password = None) :
        if not email :
            raise ValueError("You Must Have Email Address")
        email = self.normalize_email(email)
        if not full_name :
            raise ValueError("You Must Have A Name")
        email = self.normalize_email(email)
        user = self.model(email =email, full_name=full_name, is_active=True)
        user.set_password(password)
        user.save(using =self._db)
        return user
    
    def create_superuser(self, full_name, email, password = None) :
        if not email :
            raise ValueError("You Must Have Email Address")
        email = self.normalize_email(email)
        if not full_name :
            raise ValueError("You Must Have A Name")
        user = self.model(email =email, full_name=full_name, is_staff= True, is_superuser=True, is_active=True)
        user.set_password(password)
        user.save(using =self._db)
        return user
    
    
class CustomUser(AbstractBaseUser, PermissionsMixin) :
    full_name = models.CharField( max_length=150, blank=False)
    email = models.EmailField(max_length=254, blank=False, unique=True)

    #required
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name',]
    
    def __str__(self):
        return self.full_name