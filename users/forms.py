# Импортируем необходимые классы и модули из Django
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import User

# Получаем модель пользователя, которая настроена в проекте
User = get_user_model()

# Форма регистрации нового пользователя
class RegistrationForm(forms.ModelForm):
    # Поле для ввода никнейма, максимальная длина — 50 символов
    nickname = forms.CharField(max_length=50, label="Никнейм")
    # Поле для ввода email
    email = forms.EmailField(label="Email")
    # Поле для ввода пароля (с скрытыми символами)
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    # Поле для ввода подтверждения пароля (с скрытыми символами)
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)
    # Необязательное поле для загрузки аватара
    avatar = forms.ImageField(required=False, label="Аватар")

    class Meta:
        # Используем модель User для формы
        model = User
        # Указываем, какие поля будут в форме
        fields = ('nickname', 'email', 'avatar')

    # Валидация уникальности никнейма
    def clean_nickname(self):
        # Получаем значение никнейма из данных формы
        nick = self.cleaned_data['nickname']
        # Проверяем, существует ли уже пользователь с таким никнеймом
        if User.objects.filter(username=nick).exists():
            # Если существует, выбрасываем ошибку
            raise ValidationError("Этот никнейм уже занят.")
        return nick

    # Валидация совпадения паролей
    def clean(self):
        # Получаем все очищенные данные из формы
        cleaned = super().clean()
        # Извлекаем пароли
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        # Если один из паролей пуст, выбрасываем ошибку
        if not p1 or not p2:
            raise ValidationError("Оба поля пароля обязательны.")
        # Если пароли не совпадают, выбрасываем ошибку
        if p1 != p2:
            raise ValidationError("Пароли не совпадают.")
        return cleaned

    # Сохранение данных формы в объект пользователя
    def save(self, commit=True):
        # Создаём объект пользователя, но пока не сохраняем в базе данных
        user = super().save(commit=False)
        # Устанавливаем имя пользователя
        user.username = self.cleaned_data['nickname']
        # Устанавливаем никнейм пользователя
        user.nickname = self.cleaned_data['nickname']
        # Устанавливаем email пользователя
        user.email = self.cleaned_data['email']
        # Устанавливаем пароль (хешируем его с помощью set_password)
        user.set_password(self.cleaned_data['password1'])
        # Если commit=True, сохраняем пользователя в базе данных
        if commit:
            user.save()
        return user


# Форма для редактирования профиля пользователя
class ProfileForm(forms.ModelForm):
    # Поле для ввода никнейма (обновляем его)
    nickname = forms.CharField(max_length=50, label="Никнейм")
    # Поле для ввода email (обновляем его)
    email = forms.EmailField(label="Email")
    # Поле для ввода нового пароля (не обязательно)
    password = forms.CharField(label="Новый пароль", widget=forms.PasswordInput, required=False)
    # Поле для подтверждения нового пароля (не обязательно)
    password_confirm = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput, required=False)
    # Необязательное поле для загрузки нового аватара
    avatar = forms.ImageField(required=False, label="Аватар")

    class Meta:
        # Используем модель User для формы
        model = User
        # Указываем, какие поля будут в форме
        fields = ('nickname', 'email', 'avatar', 'password', 'password_confirm')

    # Валидация уникальности никнейма, исключая текущего пользователя
    def clean_nickname(self):
        # Получаем значение никнейма из данных формы
        nick = self.cleaned_data['nickname']
        # Проверяем, существует ли уже другой пользователь с таким никнеймом
        qs = User.objects.filter(username=nick).exclude(pk=self.instance.pk)
        # Если такой никнейм уже занят, выбрасываем ошибку
        if qs.exists():
            raise ValidationError("Этот никнейм уже занят.")
        return nick

    # Валидация совпадения паролей
    def clean(self):
        # Получаем все очищенные данные из формы
        cleaned = super().clean()
        # Извлекаем пароли
        p = cleaned.get('password')
        pc = cleaned.get('password_confirm')
        # Если один из паролей заполнен, проверяем совпадение
        if p or pc:
            # Если пароли не совпадают, выбрасываем ошибку
            if p != pc:
                raise ValidationError("Пароли не совпадают.")
        return cleaned

    # Сохранение данных формы в объект пользователя
    def save(self, commit=True):
        # Создаём объект пользователя, но пока не сохраняем в базе данных
        user = super().save(commit=False)
        # Устанавливаем имя пользователя
        user.username = self.cleaned_data['nickname']
        # Устанавливаем никнейм пользователя
        user.nickname = self.cleaned_data['nickname']
        # Устанавливаем email пользователя
        user.email = self.cleaned_data['email']
        # Получаем новый пароль
        new_password = self.cleaned_data.get('password')
        # Если новый пароль задан, хешируем его и сохраняем
        if new_password:
            user.set_password(new_password)
        # Если commit=True, сохраняем пользователя в базе данных
        if commit:
            user.save()
        return user
