from django import forms  # импорт модуля для работы с формами
from django.core.exceptions import ValidationError  # импорт исключения для валидации полей
from django.contrib.auth import get_user_model  # функция для получения активной модели пользователя
from django.contrib.auth.forms import PasswordResetForm  # стандартная форма сброса пароля Django
from .models import User  # импорт кастомной модели User из локального приложения

# Получаем текущую модель пользователя (наш User)
User = get_user_model()

class RegistrationForm(forms.ModelForm):  # форма регистрации нового пользователя
    nickname  = forms.CharField(
        max_length=50,
        label="Никнейм"
    )  # поле для ввода никнейма
    email     = forms.EmailField(label="Email")  # поле для ввода e-mail
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput
    )  # первое поле для пароля (скрытый ввод)
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput
    )  # второе поле для подтверждения пароля
    avatar    = forms.ImageField(
        required=False,
        label="Аватар"
    )  # поле для загрузки аватара (необязательно)

    class Meta:
        model  = User  # модель, на основе которой строится форма
        fields = ('nickname', 'email', 'avatar')  # поля, включённые в форму

    def clean_nickname(self):  # метод для проверки уникальности никнейма
        nick = self.cleaned_data['nickname']  # получаем введённое значение
        if User.objects.filter(username=nick).exists():  # проверяем в базе
            raise ValidationError("Этот никнейм уже занят.")  # если найден — ошибка
        return nick  # возвращаем валидный никнейм

    def clean(self):  # общая валидация формы
        cleaned = super().clean()  # сначала вызываем валидацию родителя
        p1 = cleaned.get('password1')  # получаем первое поле пароля
        p2 = cleaned.get('password2')  # получаем второе поле пароля
        if not p1 or not p2:  # если хотя бы одно поле пустое
            raise ValidationError("Оба поля пароля обязательны.")  # сообщаем об ошибке
        if p1 != p2:  # если пароли не совпадают
            raise ValidationError("Пароли не совпадают.")  # сообщаем об ошибке
        return cleaned  # возвращаем очищенные данные

    def save(self, commit=True):  # сохранение пользователя
        user = super().save(commit=False)  # создаём объект без сохранения в БД
        user.username = self.cleaned_data['nickname']  # задаём атрибут username
        user.nickname = self.cleaned_data['nickname']  # задаём свойство nickname
        user.email    = self.cleaned_data['email']  # задаём e-mail
        user.set_password(self.cleaned_data['password1'])  # устанавливаем пароль
        if commit:  # если нужно сразу сохранить
            user.save()  # сохраняем в БД
        return user  # возвращаем экземпляр модели


class ProfileForm(forms.ModelForm):  # форма редактирования профиля пользователя
    nickname         = forms.CharField(
        max_length=50,
        label="Никнейм"
    )  # поле для никнейма
    email            = forms.EmailField(label="Email")  # поле для e-mail
    password         = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput,
        required=False
    )  # поле для нового пароля (необязательно)
    password_confirm = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        required=False
    )  # поле для подтверждения пароля
    avatar           = forms.ImageField(
        required=False,
        label="Аватар"
    )  # поле для смены аватара

    class Meta:
        model  = User  # модель пользователя
        fields = (
            'nickname',
            'email',
            'avatar',
            'password',
            'password_confirm'
        )  # список полей формы

    def clean_nickname(self):  # проверка уникальности никнейма при редактировании
        nick = self.cleaned_data['nickname']  # введённый ник
        qs = User.objects.filter(username=nick).exclude(pk=self.instance.pk)  # исключаем текущего пользователя
        if qs.exists():  # если найден другой пользователь с таким же именем
            raise ValidationError("Этот никнейм уже занят.")  # ошибка валидации
        return nick  # валидный никнейм

    def clean(self):  # общая валидация формы
        cleaned = super().clean()  # запускаем родительскую валидацию
        p  = cleaned.get('password')  # новый пароль
        pc = cleaned.get('password_confirm')  # подтверждение пароля
        if p or pc:  # если введён хотя бы один из полей
            if p != pc:  # и они не совпадают
                raise ValidationError("Пароли не совпадают.")  # ошибка
        return cleaned  # возвращаем очищенные данные

    def save(self, commit=True):  # сохранение изменений профиля
        user = super().save(commit=False)  # создаём объект без сохранения
        user.username = self.cleaned_data['nickname']  # обновляем username
        user.nickname = self.cleaned_data['nickname']  # обновляем nickname
        user.email    = self.cleaned_data['email']  # обновляем email
        new_password = self.cleaned_data.get('password')  # получаем новый пароль
        if new_password:  # если он указан
            user.set_password(new_password)  # устанавливаем новый пароль
        if commit:  # если требуется сохранить сразу
            user.save()  # сохраняем изменения
        return user  # возвращаем пользователя


class ForgotPasswordForm(PasswordResetForm):  # форма запроса сброса пароля
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',  # включаем автозаполнение
            'class': 'form-control',  # добавляем CSS-класс для Bootstrap
            'placeholder': 'Введите ваш e-mail'  # плейсхолдер для удобства
        })
    )  # поле для ввода e-mail пользователя, который запросил сброс
