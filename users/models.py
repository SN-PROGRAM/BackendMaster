# Импортируем необходимые классы из Django
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Менеджер для модели User
class UserManager(BaseUserManager):
    # Эта настройка позволяет использовать данный менеджер в миграциях
    use_in_migrations = True

    # Основной метод для создания пользователя
    def _create_user(self, nickname, username, email, password, **extra_fields):
        # Проверяем, что никнейм предоставлен
        if not nickname:
            raise ValueError("Никнейм обязателен")
        # Проверяем, что username предоставлен
        if not username:
            raise ValueError("Username обязателен")
        # Нормализуем email (приводим к нижнему регистру и т.д.)
        email = self.normalize_email(email)
        # Создаем нового пользователя
        user = self.model(nickname=nickname, username=username, email=email, **extra_fields)
        # Устанавливаем пароль (с хешированием)
        user.set_password(password)
        # Сохраняем пользователя в базе данных
        user.save(using=self._db)
        return user

    # Метод для создания обычного пользователя
    def create_user(self, nickname, username, email=None, password=None, **extra_fields):
        # Устанавливаем значения по умолчанию для полей is_staff и is_superuser
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        # Создаем пользователя через метод _create_user
        return self._create_user(nickname, username, email, password, **extra_fields)

    # Метод для создания суперпользователя
    def create_superuser(self, nickname, username, email=None, password=None, **extra_fields):
        # Устанавливаем значения по умолчанию для полей is_staff и is_superuser как True для суперпользователя
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # Создаем суперпользователя через метод _create_user
        return self._create_user(nickname, username, email, password, **extra_fields)


# Модель пользователя, которая расширяет стандартную модель AbstractUser
class User(AbstractUser):
    # Поле для хранения уникального никнейма
    nickname = models.CharField(max_length=50, unique=True, verbose_name="Никнейм", help_text="Будет использоваться как основной логин")
    # Поле для аватара пользователя, изображение может быть пустым
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    # Указываем, что поле username для входа заменено на поле nickname
    USERNAME_FIELD = 'nickname'
    # Указываем дополнительные обязательные поля для создания пользователя
    REQUIRED_FIELDS = ['username', 'email']
    # Присваиваем модели менеджер UserManager
    objects = UserManager()

    # Метод, который определяет, как будет отображаться объект пользователя в админке и других местах
    def __str__(self):
        return self.nickname
