# Импортируем модуль models для создания моделей Django
from django.db import models

# Импортируем настройки проекта, в частности для доступа к модели пользователя
from django.conf import settings

# Модель для курсов
class Course(models.Model):
    title = models.CharField(max_length=200)  # Название курса (текст до 200 символов)
    description = models.TextField()  # Полное описание курса
    instructor = models.ForeignKey(  # Преподаватель (внешний ключ на пользователя)
        settings.AUTH_USER_MODEL,  # Ссылка на модель пользователя из настроек
        on_delete=models.CASCADE,  # При удалении пользователя — удаляются его курсы
        related_name='courses'  # Позволяет получить все курсы пользователя: user.courses.all()
    )
    category = models.CharField(max_length=100, default="Uncategorized")  # Категория курса
    image = models.URLField(blank=True, null=True)  # Ссылка на изображение курса (необязательное поле)
    is_published = models.BooleanField(default=False)  # Флаг публикации курса
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания курса (устанавливается автоматически)
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего изменения (обновляется при сохранении)

    def __str__(self):
        return self.title  # Отображение объекта курса в админке и других местах — по названию

# Модель для записей пользователей на курсы
class Enrollment(models.Model):
    user = models.ForeignKey(  # Пользователь, который записался на курс
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE  # При удалении пользователя удаляются и его записи
    )
    course = models.ForeignKey(  # Курс, на который он записался
        Course,
        on_delete=models.CASCADE  # При удалении курса удаляются и записи
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)  # Дата и время записи на курс
    completed_lessons = models.ManyToManyField(  # Завершённые уроки
        'Lesson',  # Ссылка на модель Lesson (в кавычках, т.к. она определена позже)
        blank=True,  # Поле необязательное
        related_name='completed_by'  # Позволяет узнать, кто завершил урок: lesson.completed_by.all()
    )

    class Meta:
        unique_together = ('user', 'course')  # Один пользователь может быть записан на курс только один раз

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"  # Строковое представление объекта

# Модель для уроков, входящих в курс
class Lesson(models.Model):
    course = models.ForeignKey(  # Ссылка на курс, к которому относится урок
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'  # Позволяет получить все уроки курса: course.lessons.all()
    )
    title = models.CharField(max_length=200)  # Название урока
    content = models.TextField(  # Дополнительные заметки к уроку
        blank=True,
        help_text="Дополнительные заметки к уроку (опционально)"
    )
    material = models.TextField(  # Основной теоретический материал
        blank=True,
        help_text="Материалы урока (например, теория)"
    )
    task = models.TextField(  # Задание для ученика
        blank=True,
        help_text="Задание для пользователя"
    )
    solution = models.TextField(  # Решение (для преподавателя)
        blank=True,
        help_text="Правильное решение (скрыто от пользователя)"
    )
    video = models.URLField(  # Ссылка на обучающее видео
        blank=True,
        null=True
    )
    order = models.PositiveIntegerField(default=0)  # Порядок отображения урока в курсе
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания урока

    def __str__(self):
        return self.title  # Отображение объекта урока в интерфейсе

    class Meta:
        ordering = ['order']  # Уроки будут автоматически сортироваться по полю order
