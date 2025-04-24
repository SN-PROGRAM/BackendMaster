from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, ProfileForm
from django.contrib.auth import update_session_auth_hash


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Добро пожаловать")
            return redirect('profile')
        else:
            messages.error(request, "Пожалуйста, исправьте данные")
    else:
        form = RegistrationForm()
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Вы успешно вошли.")
            return redirect('home')  # Перенаправление на главную страницу
        else:
            messages.error(request, "Неправильный логин или пароль.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect('login')


@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Профиль успешно обновлён.")
            return redirect('profile')
        else:
            messages.error(request, "Пожалуйста, введите корректные данные")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})