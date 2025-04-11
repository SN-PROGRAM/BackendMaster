from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Course, Enrollment
from .forms import CourseForm


# Отображение главной страницы
def home(request):
    return render(request, 'base.html')


# Список курсов. Для обычных пользователей — только опубликованные, для админов — все.
class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        # Администраторы видят все курсы
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Course.objects.all()
        # Остальные видят только опубликованные курсы
        return Course.objects.filter(is_published=True)


# Детальное отображение курса с проверкой, записан ли пользователь на него
class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Добавляем информацию о том, записан ли пользователь на курс
            context['is_enrolled'] = Enrollment.objects.filter(
                user=self.request.user, course=self.object
            ).exists()
        return context


# Создание нового курса. Доступно только преподавателям (is_staff)
class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    fields = ['title', 'description', 'category', 'image']
    template_name = 'courses/course_form.html'

    def test_func(self):
        # Разрешено только сотрудникам/преподавателям
        return self.request.user.is_staff

    def form_valid(self, form):
        # Устанавливаем текущего пользователя как преподавателя курса
        form.instance.instructor = self.request.user
        return super().form_valid(form)


# Редактирование курса. Доступно преподавателю курса или админу
class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    fields = ['title', 'description', 'category', 'image', 'is_published']
    template_name = 'courses/course_form.html'

    def test_func(self):
        course = self.get_object()
        # Проверка прав: автор курса или админ
        return self.request.user == course.instructor or self.request.user.is_staff


# Удаление курса. Доступно преподавателю курса или админу
class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('courses:course_list')

    def test_func(self):
        course = self.get_object()
        # Проверка прав: автор курса или админ
        return self.request.user == course.instructor or self.request.user.is_staff


# Запись на курс. Только для авторизованных пользователей
@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)

    # Нельзя записаться на неопубликованный курс
    if not course.is_published:
        messages.error(request, "This course is not available for enrollment.")
        return redirect('courses:course_list')

    # Проверка: пользователь уже записан?
    if Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.info(request, "You are already enrolled in this course.")
    else:
        # Создание записи об участии
        Enrollment.objects.create(user=request.user, course=course)
        messages.success(request, f"You have successfully enrolled in {course.title}!")

    return redirect('courses:course_detail', pk=course.pk)
