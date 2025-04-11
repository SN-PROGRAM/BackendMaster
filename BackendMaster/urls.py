from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from courses import views as course_views

urlpatterns = [
    path('', course_views.CourseListView.as_view(), name='home'),  # Сделал главную страницу активной через CourseListView
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),
    path('accounts/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)