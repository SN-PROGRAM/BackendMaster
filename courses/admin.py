# Импортируем модуль admin из django.contrib, чтобы настраивать административный интерфейс
from django.contrib import admin

# Импортируем модели Course, Lesson и Enrollment из текущего пакета (приложения)
from .models import Course, Lesson, Enrollment

# Определяем класс для отображения уроков внутри курсов на странице редактирования курса
class LessonInline(admin.TabularInline):
    model = Lesson  # Указываем, что inline-форма будет связана с моделью Lesson
    extra = 1  # Количество пустых форм для добавления новых уроков (по умолчанию одна)
    fields = ['title', 'material', 'task', 'solution', 'video', 'order']  # Поля, отображаемые в форме

# Регистрируем модель Course в административной панели с использованием кастомного класса CourseAdmin
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'is_published', 'created_at')  # Колонки, отображаемые в списке курсов
    list_filter = ('is_published',)  # Фильтрация по полю публикации
    search_fields = ('title', 'description')  # Поля, по которым можно искать курсы
    date_hierarchy = 'created_at'  # Позволяет навигацию по датам в админке
    inlines = [LessonInline]  # Встраиваем уроки в форму редактирования курсов

# Регистрируем модель Lesson в админке с использованием кастомного класса LessonAdmin
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at')  # Колонки в списке уроков
    list_filter = ('course',)  # Фильтр по курсу
    search_fields = ('title', 'content', 'material', 'task')  # Поля для поиска уроков
    fieldsets = (  # Разделение формы редактирования на группы полей
        (None, {
            'fields': ('title', 'course', 'order')  # Основные поля
        }),
        ('Содержимое урока', {
            'fields': ('material', 'task', 'solution', 'video', 'content')  # Содержательная часть урока
        }),
    )

# Регистрируем модель Enrollment (запись на курс) с кастомным отображением
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at')  # Колонки в списке записей на курс
    list_filter = ('course',)  # Фильтр по курсу
    search_fields = ('user__username',)  # Поиск по имени пользователя (через связь user)
