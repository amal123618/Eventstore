from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
User = get_user_model()
class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    # phone = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password']