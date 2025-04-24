# Импортируем необходимые функции и классы
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, ProfileForm
from django.contrib.auth import update_session_auth_hash

# Функция для регистрации пользователя
def signup(request):
    if request.method == 'POST':  # Если был отправлен POST-запрос
        form = RegistrationForm(request.POST, request.FILES)  # Создаём форму с данными из POST-запроса и файлами
        if form.is_valid():  # Если форма валидна
            user = form.save()  # Сохраняем пользователя
            login(request, user)  # Выполняем вход в систему
            messages.success(request, "Добро пожаловать")  # Отправляем сообщение об успешной регистрации
            return redirect('profile')  # Перенаправляем на страницу профиля
        else:
            messages.error(request, "Пожалуйста, исправьте данные")  # Если форма невалидна, выводим ошибку
    else:
        form = RegistrationForm()  # Если запрос GET, создаём пустую форму
    return render(request, 'users/signup.html', {'form': form})  # Рендерим шаблон с формой

# Функция для входа в систему
def login_view(request):
    if request.method == 'POST':  # Если был отправлен POST-запрос
        form = AuthenticationForm(request, data=request.POST)  # Создаём форму для аутентификации
        if form.is_valid():  # Если форма валидна
            user = form.get_user()  # Получаем пользователя из формы
            login(request, user)  # Выполняем вход в систему
            messages.success(request, "Вы успешно вошли.")  # Отправляем сообщение об успешном входе
            return redirect('home')  # Перенаправляем на главную страницу
        else:
            messages.error(request, "Неправильный логин или пароль.")  # Если форма невалидна, выводим ошибку
    else:
        form = AuthenticationForm()  # Если запрос GET, создаём пустую форму
    return render(request, 'users/login.html', {'form': form})  # Рендерим шаблон с формой

# Функция для выхода из системы (требуется авторизация)
@login_required
def logout_view(request):
    logout(request)  # Выход из системы
    messages.info(request, "Вы вышли из аккаунта.")  # Отправляем сообщение о выходе
    return redirect('login')  # Перенаправляем на страницу входа

# Функция для отображения профиля пользователя (требуется авторизация)
@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})  # Рендерим шаблон профиля пользователя

# Функция для редактирования профиля (требуется авторизация)
@login_required
def edit_profile(request):
    if request.method == 'POST':  # Если был отправлен POST-запрос
        form = ProfileForm(request.POST, request.FILES, instance=request.user)  # Создаём форму с данными из POST-запроса и файлом
        if form.is_valid():  # Если форма валидна
            user = form.save()  # Сохраняем изменения
            update_session_auth_hash(request, user)  # Обновляем сессионный хеш, чтобы не выкинуло из сессии после смены пароля
            messages.success(request, "Профиль успешно обновлён.")  # Отправляем сообщение об успешном обновлении
            return redirect('profile')  # Перенаправляем на страницу профиля
        else:
            messages.error(request, "Пожалуйста, введите корректные данные")  # Если форма невалидна, выводим ошибку
    else:
        form = ProfileForm(instance=request.user)  # Если запрос GET, создаём форму с данными текущего пользователя
    return render(request, 'users/edit_profile.html', {'form': form})  # Рендерим шаблон редактирования профиля
