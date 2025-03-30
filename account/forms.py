from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import MyUser
from django.contrib.auth import authenticate


class RegisterForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '请输入用户名'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '请输入密码'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '请确认密码'
        })


class MyAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder':'请输入用户名',
            'autocomplete':'username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder':'请输入密码',
            'autocomplete':'current_password'
        })
