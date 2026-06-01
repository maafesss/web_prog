from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm
)
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label="Имя пользователя",
        validators=[
            RegexValidator(
                regex='^[A-ZА-Я][a-zа-яё]*$',
                message='Только буквы, первая заглавная!'
            )
        ],
        widget=forms.TextInput(attrs={'placeholder': 'Например: V'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'example@nightcity.com'})
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Минимум 8 символов'}),
        min_length=8
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'placeholder': 'Введите ваш логин'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'})
    )