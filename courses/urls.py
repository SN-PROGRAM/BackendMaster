from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'), # Главная страница списка курсов
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'), # Детальная страница конкретного курса (по ID)
    path('create/', views.CourseCreateView.as_view(), name='course_create'), # Страница создания нового курса (доступна только преподавателям)
    path('<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'), # Страница редактирования курса по ID (если преподаватель или админ)
    path('<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'), # Страница подтверждения удаления курса (если преподаватель или админ)
    path('<int:pk>/enroll/', views.enroll_course, name='enroll_course'), # Обработка записи пользователя на курс (по ID курса)
]
