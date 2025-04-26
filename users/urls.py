from django.urls import path  # импорт функции path для определения маршрутов
from . import views      # импорт модуля views из текущего приложения

app_name = 'users'  # namespace для маршрутов приложения, чтобы избежать конфликтов имён

urlpatterns = [  # список URL-шаблонов для приложения users
    # Аутентификация и профиль пользователя

    path('login/',        views.login_view,   name='login'),         # маршрут для страницы входа
    path('signup/',       views.signup,       name='signup'),        # маршрут для страницы регистрации
    path('logout/',       views.logout_view,  name='logout'),        # маршрут для выхода из аккаунта
    path('profile/',      views.profile_view, name='profile'),       # маршрут для просмотра профиля
    path('edit-profile/', views.edit_profile, name='edit_profile'),  # маршрут для редактирования профиля

    # Сброс пароля по e-mail (Password Reset Flow)
    path(
        'password_reset/',
        views.ForgotPasswordView.as_view(),
        name='password_reset'  # первая страница: форма ввода e-mail
    ),
    path(
        'password_reset/done/',
        views.ForgotPasswordDoneView.as_view(),
        name='password_reset_done'  # страница «Письмо отправлено»
    ),
    path(
        'reset/<uidb64>/<token>/',
        views.ForgotPasswordConfirmView.as_view(),
        name='password_reset_confirm'  # страница установки нового пароля
    ),
    path(
        'reset/done/',
        views.ForgotPasswordCompleteView.as_view(),
        name='password_reset_complete'  # страница завершения сброса пароля
    ),
]  # конец списка urlpatterns
