from django import forms 
from django.core.exceptions import ValidationError 
from django.contrib.auth.models import User 

class RegistrationForm(forms.Form):
    fullname = forms.CharField(max_length=100, required=True, label='FullName')
    email = forms.EmailField(max_length=100, required=True, label='Email')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, label='Confirm Password')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('Password and Confirm Password  are does not matched') 
        return confirm_password 
    
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True, label='Email')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Password')

    