from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()
class RegistrationForm(forms.ModelForm):
    nickname = forms.CharField(max_length=50, label="Никнейм")
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False, label="Аватар")

    class Meta:
        model = User
        fields = ('nickname', 'email', 'avatar')

    def clean_nickname(self):
        nick = self.cleaned_data['nickname']
        if User.objects.filter(username=nick).exists():
            raise ValidationError("Этот никнейм уже занят.")
        return nick

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if not p1 or not p2:
            raise ValidationError("Оба поля пароля обязательны.")
        if p1 != p2:
            raise ValidationError("Пароли не совпадают.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['nickname']
        user.nickname = self.cleaned_data['nickname']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    nickname = forms.CharField(max_length=50, label="Никнейм")
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Новый пароль", widget=forms.PasswordInput, required=False)
    password_confirm = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput, required=False)
    avatar = forms.ImageField(required=False, label="Аватар")

    class Meta:
        model = User
        fields = ('nickname', 'email', 'avatar', 'password', 'password_confirm')

    def clean_nickname(self):
        nick = self.cleaned_data['nickname']
        qs = User.objects.filter(username=nick).exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Этот никнейм уже занят.")
        return nick

    def clean(self):
        cleaned = super().clean()
        p = cleaned.get('password')
        pc = cleaned.get('password_confirm')
        if p or pc:
            if p != pc:
                raise ValidationError("Пароли не совпадают.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['nickname']
        user.nickname = self.cleaned_data['nickname']
        user.email = self.cleaned_data['email']
        new_password = self.cleaned_data.get('password')
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user