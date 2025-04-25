# Импорт функции path, необходимой для определения маршрутов URL
from django.urls import path

# Импортируем views из текущего пакета — здесь находятся классы и функции обработки запросов
from . import views

# Указываем пространство имён для приложения 'courses' — это помогает избежать конфликтов имён URL при использовании include()
app_name = 'courses'

# Список маршрутов URL, которые обрабатываются в этом приложении
urlpatterns = [

    # Главная страница со списком всех курсов
    path('', views.CourseListView.as_view(), name='course_list'),

    # Страница с деталями конкретного курса по его ID (pk)
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),

    # Страница обучения, где пользователь может просматривать материалы курса
    path('<int:pk>/learn/', views.CourseLearnView.as_view(), name='course_learn'),

    # Страница создания нового курса
    path('create/', views.CourseCreateView.as_view(), name='course_create'),

    # Страница редактирования существующего курса по его ID
    path('<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),

    # Страница удаления курса по его ID
    path('<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),

    # Маршрут для записи пользователя на курс (обрабатывается функцией, а не классом)
    path('<int:pk>/enroll/', views.enroll_course, name='enroll_course'),

    # Страница создания нового урока внутри конкретного курса (по ID курса)
    path('<int:pk>/lesson/create/', views.LessonCreateView.as_view(), name='lesson_create'),

    # Страница редактирования конкретного урока в определённом курсе (указаны оба ID: курса и урока)
    path('<int:course_pk>/lesson/<int:lesson_pk>/edit/', views.LessonUpdateView.as_view(), name='lesson_edit'),

    # Страница удаления конкретного урока из курса (также указаны ID курса и урока)
    path('<int:course_pk>/lesson/<int:lesson_pk>/delete/', views.LessonDeleteView.as_view(), name='lesson_delete'),
]