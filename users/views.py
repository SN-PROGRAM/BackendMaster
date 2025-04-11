from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserForm  # Форма регистрации
from django.contrib.auth.models import User


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            # Вытаскиваем данные из формы
            nickname = form.cleaned_data['nickname']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']

            if password != password_confirm:
                form.add_error('password_confirm', 'Пароли не совпадают')
            else:
                # Создаем пользователя
                user = User(
                    username=nickname,
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name']
                )
                user.set_password(password)  # вот этот метод должен быть
                user.save()

                # Здесь можно добавить сохранение аватара, если он отдельно
                return redirect('login')  # или куда нужно
    else:
        form = UserForm()

    return render(request, 'users/signup.html', {'form': form})


# Вход
def login_view(request):
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
        form = UserForm(request.POST, request.FILES, instance=request.user)  # Передаем request.FILES для обработки изображений
        if form.is_valid():# Обработка аватара и никнейма
            user = form.save(commit=False)# Если пароль был введен, то его нужно обновить
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)  # Устанавливаем новый пароль, если он есть
            user.save()

            messages.success(request, "Ваш профиль успешно обновлен!")
            return redirect('profile')  # Перенаправляем на страницу профиля
    else:
        form = UserForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})

def profile_view(request):
    return render(request, 'users/profile.html')  # шаблон для отображения профиля