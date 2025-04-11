from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    nickname = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.username
