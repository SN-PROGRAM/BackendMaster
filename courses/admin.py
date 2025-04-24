from django.contrib import admin
from .models import Course, Lesson, Enrollment

# Отображение уроков внутри курсов (inline-форма)
class LessonInline(admin.TabularInline):
    model = Lesson  # Модель, которую встраиваем
    extra = 1  # Показывать 1 пустую форму для добавления нового урока

# Админка для курсов
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'is_published', 'created_at')  # Отображаемые поля
    list_filter = ('is_published',)  # Фильтрация только по опубликованности
    search_fields = ('title', 'description')  # Поиск по названию и описанию
    date_hierarchy = 'created_at'  # Навигация по датам создания
    inlines = [LessonInline]  # Вставка уроков прямо в админку курсов

# Админка для уроков
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')  # Отображаемые поля (убрали created_at, так как его нет в модели)
    list_filter = ('course',)  # Фильтрация по курсу
    search_fields = ('title', 'content')  # Поиск по названию и содержанию

# Админка для записей на курсы
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at')  # Отображаемые поля
    list_filter = ('course',)  # Фильтрация по курсу
    search_fields = ('user__username',)  # Поиск по имени пользователя