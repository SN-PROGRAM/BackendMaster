from django.db import models

class User(models.Model):  # Модель пользователя
    nickname = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=254)
    password = models.CharField(max_length=128)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.nickname
