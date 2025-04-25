# Импортируем модуль forms из Django, чтобы создавать и использовать формы
from django import forms

# Импортируем модель Course из текущего приложения
from .models import Course

# Создаём форму на основе модели Course
class CourseForm(forms.ModelForm):  # Наследуемся от ModelForm, чтобы форма автоматически строилась по модели
    class Meta:  # Внутренний класс, в котором указываются настройки формы
        model = Course  # Указываем модель, на основе которой будет строиться форма
        fields = ['title', 'description', 'instructor', 'category', 'image']  
        # Указываем, какие поля модели должны быть включены в форму
