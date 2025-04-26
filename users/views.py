# Импорт функций для рендеринга шаблонов и перенаправления
from django.shortcuts import render, redirect
# Импорт модуля для flash-сообщений пользователю
from django.contrib import messages
# Импорт функций для входа и выхода пользователя
from django.contrib.auth import login, logout
# Декоратор для защиты представлений, требующих авторизации
from django.contrib.auth.decorators import login_required
# Форма для аутентификации (входа)
from django.contrib.auth.forms import AuthenticationForm
# Импорт пользовательских форм регистрации и редактирования профиля
from .forms import RegistrationForm, ProfileForm
# Функция для обновления хеша сессии после смены пароля
from django.contrib.auth import update_session_auth_hash
# Утилита для отложенного reverse по имени URL
from django.urls import reverse_lazy
# Импорт стандартных CBV для сброса пароля
from django.contrib.auth.views import (
    PasswordResetView,         # отображает форму запроса сброса пароля
    PasswordResetDoneView,     # показывает сообщение об отправке письма
    PasswordResetConfirmView,  # форма ввода нового пароля по ссылке
    PasswordResetCompleteView  # финальное подтверждение успешного сброса
)
# Импорт кастомной формы для запроса сброса пароля
from .forms import ForgotPasswordForm


# Представление регистрации нового пользователя
def signup(request):
    if request.method == 'POST':  # если отправлен POST-запрос
        # создаём форму с данными и файлами из запроса
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():  # проверяем валидность формы
            user = form.save()  # сохраняем нового пользователя
            login(request, user)  # автоматически логиним созданного пользователя
            messages.success(request, "Добро пожаловать")  # сообщаем об успехе
            return redirect('profile')  # перенаправляем на страницу профиля
        else:
            messages.error(request, "Пожалуйста, исправьте данные")  # сообщаем об ошибках ввода
    else:
        form = RegistrationForm()  # при GET-запросе создаём пустую форму
    # отображаем шаблон регистрации с формой
    return render(request, 'users/signup.html', {'form': form})


# Представление для входа пользователя
def login_view(request):
    if request.method == 'POST':  # если отправлен POST-запрос
        # создаём форму аутентификации с переданными данными
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():  # проверяем корректность введённых данных
            user = form.get_user()  # получаем объект пользователя
            login(request, user)  # выполняем вход в систему
            messages.success(request, "Вы успешно вошли.")  # сообщаем об успешном входе
            return redirect('home')  # перенаправляем на главную страницу
        else:
            messages.error(request, "Неправильный логин или пароль.")  # сообщаем об ошибке
    else:
        form = AuthenticationForm()  # при GET-запросе создаём пустую форму входа
    # отображаем шаблон входа с формой
    return render(request, 'users/login.html', {'form': form})


# Представление для выхода из системы (только для авторизованных)
@login_required
def logout_view(request):
    logout(request)  # выполняем выход пользователя
    messages.info(request, "Вы вышли из аккаунта.")  # сообщаем об успешном выходе
    return redirect('users:login')  # перенаправляем на страницу входа


# Представление профиля пользователя (только для авторизованных)
@login_required
def profile_view(request):
    # отображаем шаблон профиля, передавая объект текущего пользователя
    return render(request, 'users/profile.html', {'user': request.user})


# Представление для редактирования профиля (только для авторизованных)
@login_required
def edit_profile(request):
    if request.method == 'POST':  # если отправлен POST-запрос
        # создаём форму с данными из запроса, файлов и текущего пользователя
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():  # проверяем валидность формы
            user = form.save()  # сохраняем изменения профиля
            # обновляем хеш сессии, чтобы не выкинуло после смены пароля
            update_session_auth_hash(request, user)
            messages.success(request, "Профиль успешно обновлён.")  # сообщаем об успехе
            return redirect('profile')  # перенаправляем на страницу профиля
        else:
            messages.error(request, "Пожалуйста, введите корректные данные")  # сообщаем об ошибке
    else:
        form = ProfileForm(instance=request.user)  # при GET-запросе заполняем форму текущими данными
    # отображаем шаблон редактирования профиля с формой
    return render(request, 'users/edit_profile.html', {'form': form})


# CBV для отправки письма со ссылкой на сброс пароля
class ForgotPasswordView(PasswordResetView):
    template_name = 'users/reset/password_reset_form.html'         # шаблон формы запроса
    form_class = ForgotPasswordForm                               # кастомная форма запроса пароля
    email_template_name = 'users/reset/password_reset_email.html' # шаблон письма
    # success_url — куда редирект после успешной отправки письма
    success_url = reverse_lazy('users:password_reset_done')


# CBV, отображающий страницу с уведомлением об отправке письма
class ForgotPasswordDoneView(PasswordResetDoneView):
    template_name = 'users/reset/password_reset_done.html'        # шаблон подтверждения отправки


class ForgotPasswordConfirmView(PasswordResetConfirmView):
    template_name = 'users/reset/password_reset_confirm.html'


# CBV для финального подтверждения успешного сброса пароля
class ForgotPasswordCompleteView(PasswordResetCompleteView):
    template_name = 'users/reset/password_reset_complete.html'
    success_url = reverse_lazy('users:login')
