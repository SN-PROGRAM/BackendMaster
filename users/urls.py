from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Вход
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login'), name='logout'),
    path('profile/', views.profile_view, name='profile'),  # Путь для отображения профиля пользователя
    path('edit-profile/', views.edit_profile, name='edit_profile'),  # Путь для редактирования профиля
    ]