from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, nickname, username, email, password, **extra_fields):
        if not nickname:
            raise ValueError("Никнейм обязателен")
        if not username:
            raise ValueError("Username обязателен")
        email = self.normalize_email(email)
        user = self.model(nickname=nickname, username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, nickname, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(nickname, username, email, password, **extra_fields)

    def create_superuser(self, nickname, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(nickname, username, email, password, **extra_fields)


class User(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True, verbose_name="Никнейм", help_text="Будет использоваться как основной логин")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['username', 'email']
    objects = UserManager()

    def __str__(self):
        return self.nickname
