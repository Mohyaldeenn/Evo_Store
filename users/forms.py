from django import forms
from .models import CustomUser


class RegistrationForm(forms.ModelForm) :
    password = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder' : "Enter Your password",
        'class': "form-control",
    }))
    conform_password = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder' : "Enter Your password",
    }))
    class Meta :
        model = CustomUser
        fields = ["full_name", "email", "password"]
    
    def __init__(self, *args, **kwargs) :
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs['placeholder'] = "Enter Your Full Name"
        self.fields["email"].widget.attrs['placeholder'] = "Enter Your Email"
        for field in self.fields :
            self.fields[field].widget.attrs["class"] = 'form-control'