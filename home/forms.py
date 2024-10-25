from django import forms
from django.contrib.auth.models import User
from .models import Album, Image
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'confirm_password', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'caption']


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input-group input-field',
        'required': True,
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input-group input-field',
        'required': True,
    }))

class CustomRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input-group input-field',
        'required': True,
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input-group input-field',
        'required': True,
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input-group input-field',
        'required': True,
    }))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']