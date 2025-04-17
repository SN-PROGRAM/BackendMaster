from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserForm
from django.contrib.auth.models import User  # Или ваша кастомная модель пользователя


def signup(request):  # Регистрация
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация прошла успешно! Теперь вы можете войти в систему.")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):  # Вход в систему
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"С возвращением, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваш профиль успешно обновлен!")
            return redirect('profile')
    else:
        form = UserForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})



def profile_view(request):  # Отображение профиля
    return render(request, 'users/profile.html')
