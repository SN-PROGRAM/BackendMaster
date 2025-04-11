from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from courses import views as course_views

urlpatterns = [
    path('', course_views.CourseListView.as_view(), name='home'),  # Главная страница сайта — список всех курсов (через CourseListView)
    path('admin/', admin.site.urls),  # Админ-панель Django (доступна по адресу /admin/)
    path('courses/', include('courses.urls')),  # Подключение маршрутов из приложения "courses" (курсы)
    path('accounts/', include('users.urls')),  # Подключение маршрутов из приложения "users" (регистрация, вход и т.д.)
]

# Если включен режим отладки (DEBUG = True), подключаем обработку медиафайлов (например, изображений курсов)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
