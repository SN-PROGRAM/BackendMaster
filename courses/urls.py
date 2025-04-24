# Импортируем функцию path для настройки маршрутов
from django.urls import path

# Импортируем представления из текущего модуля
from . import views

# Пространство имён для приложения 'courses' — полезно при использовании {% url %} и include()
app_name = 'courses'

# Список маршрутов (URL-адресов), связанных с этим приложением
urlpatterns = [

    # Главная страница курсов — список всех курсов
    path('', views.CourseListView.as_view(), name='course_list'),

    # Детальный просмотр курса по его id (pk = primary key)
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),

    # Страница создания нового курса
    path('create/', views.CourseCreateView.as_view(), name='course_create'),

    # Страница редактирования курса по id
    path('<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),

    # Страница удаления курса по id
    path('<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),

    # Запись пользователя на курс
    path('<int:pk>/enroll/', views.enroll_course, name='enroll_course'),

    # Страница обучения (просмотр контента курса)
    path('<int:pk>/learn/', views.CourseLearnView.as_view(), name='course_learn'),

    # Создание нового урока внутри курса
    path('<int:pk>/lessons/create/', views.LessonCreateView.as_view(), name='lesson_create'),

    # Обновление урока внутри конкретного курса
    path('<int:course_pk>/lessons/<int:lesson_pk>/update/', views.LessonUpdateView.as_view(), name='lesson_update'),

    # Удаление урока внутри конкретного курса
    path('<int:course_pk>/lessons/<int:lesson_pk>/delete/', views.LessonDeleteView.as_view(), name='lesson_delete'),
]
