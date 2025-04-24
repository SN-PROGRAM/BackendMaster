# Импортируем необходимые классы и функции для работы с URL
from django.urls import path
from . import views  # Импортируем представления (views) из текущего приложения

# Список URL-шаблонов для обработки различных запросов
urlpatterns = [
    # Путь для страницы входа (выполняется с использованием views.login_view)
    path('login/', views.login_view, name='login'),  # Вход

    # Путь для страницы регистрации (выполняется с использованием views.signup)
    path('signup/', views.signup, name='signup'),  # Регистрация

    # Путь для выхода из аккаунта (выполняется с использованием views.logout_view)
    path('logout/', views.logout_view, name='logout'),  # Путь для выхода из аккаунта

    # Путь для отображения страницы профиля пользователя (выполняется с использованием views.profile_view)
    path('profile/', views.profile_view, name='profile'),  # Путь для отображения профиля пользователя

    # Путь для страницы редактирования профиля (выполняется с использованием views.edit_profile)
    path('edit-profile/', views.edit_profile, name='edit_profile'),  # Путь для редактирования профиля
]
