# users/forms.py
from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    nickname = forms.CharField(max_length=50, label="Никнейм")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль', required=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label='Подтверждение пароля', required=False)
    avatar = forms.ImageField(required=False, label="Аватар")

    class Meta:
        model = User
        fields = [
            'nickname', 'email', 'avatar','password', 'password_confirm']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        is_creation = not self.instance.pk
        for field in ('password', 'password_confirm'):
            self.fields[field].required = is_creation

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('password_confirm')
        if password or confirm:
            if password != confirm:
                raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Синхронизируем nickname и username
        user.nickname = self.cleaned_data['nickname']
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class RegistrationForm(UserForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = True
        self.fields['password_confirm'].required = True

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if User.objects.filter(username=nickname).exists():
            raise forms.ValidationError("Этот ник уже занят.")
        return nickname


# users/views.py
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import RegistrationForm, UserForm


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Проверьте корректность введённых данных.")
    else:
        form = RegistrationForm()
    return render(request, 'users/signup.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлён.")
            return redirect('profile')
        else:
            messages.error(request, "Проверьте корректность введённых данных.")
    else:
        form = UserForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})
