from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Вход
    path('signup/', views.signup, name='signup'), # Регистрация
    path('logout/', views.logout_view,name='logout'), # Путь для выхода из аккаунта
    path('profile/', views.profile_view, name='profile'),  # Путь для отображения профиля пользователя
    path('edit-profile/', views.edit_profile, name='edit_profile'),  # Путь для редактирования профиля
    ]