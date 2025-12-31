from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model=User
        fields =['username','password','password_confirm']
    
    password=forms.CharField(widget=forms.PasswordInput, label="password")
    password_confirm=forms.CharField(widget=forms.PasswordInput, label="confirm password")
    
    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data.get('password')
        password_confirm=cleaned_data.get('password_confirm')
        # checking the passwords
        if password and password_confirm and password != password_confirm :
            raise forms.ValidationError("passwords are not same")
        return cleaned_data
    
    