from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('create/', views.CourseCreateView.as_view(), name='course_create'),
    path('<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),
    path('<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    path('<int:pk>/enroll/', views.enroll_course, name='enroll_course'),
    path('<int:pk>/learn/', views.CourseLearnView.as_view(), name='course_learn'),
    path('<int:pk>/lessons/create/', views.LessonCreateView.as_view(), name='lesson_create'),
    path('<int:course_pk>/lessons/<int:lesson_pk>/update/', views.LessonUpdateView.as_view(), name='lesson_update'),
    path('<int:course_pk>/lessons/<int:lesson_pk>/delete/', views.LessonDeleteView.as_view(), name='lesson_delete'),
]