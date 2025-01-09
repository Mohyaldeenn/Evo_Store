from django import forms
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm) :
    password = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder' : "Enter Your password",
        'class': "form-control",
    }), validators= [validate_password],)
    confirm_password = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder' : "Confirm Your password",
    }))
    class Meta :
        model = CustomUser
        fields = ["full_name", "email", "password" ]

    
    def clean(self) :
        clean_data = super(RegistrationForm, self).clean()
        password = clean_data.get("password")
        confirm_password = clean_data.get("confirm_password")
        if  password != confirm_password :
            raise forms.ValidationError(f" passwords does not match !!")
        return clean_data
        
    
    def __init__(self, *args, **kwargs) :
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs['placeholder'] = "Enter Your Full Name"
        self.fields["email"].widget.attrs['placeholder'] = "Enter Your Email"
        for field in self.fields :
            self.fields[field].widget.attrs["class"] = 'form-control'
    
        