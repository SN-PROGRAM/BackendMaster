from django import forms
from django import forms
from .models import User

class UserForm(forms.ModelForm):
    nickname = forms.CharField(max_length=50, required=True, label="Username")
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Пароль')
    password_confirm = forms.CharField(widget=forms.PasswordInput(), required=True, label='Подтверждение пароля')
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['nickname', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'avatar']

    def clean_username(self): # Сначала проверим, есть ли значение в username и nickname
        cleaned_username = self.cleaned_data.get('username', '')
        cleaned_nickname = self.cleaned_data.get('nickname', '')# Если есть значение в nickname, добавляем его к username
        if cleaned_nickname:
            cleaned_username = f"{cleaned_username} {cleaned_nickname}"

        # Возвращаем объединённое значение
        return cleaned_username.strip()

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают.")

        return password_confirm
