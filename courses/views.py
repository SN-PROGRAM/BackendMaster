from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .models import Course, Enrollment, Lesson
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
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Course.objects.all()
        return Course.objects.filter(is_published=True)

# Детальное отображение курса с проверкой, записан ли пользователь на него
class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'reset_progress' in request.POST:
            enrollment = Enrollment.objects.get(user=self.request.user, course=self.object)
            enrollment.completed_lessons.clear()
            messages.success(request, "Ваш прогресс по курсу сброшен.")
            return redirect('courses:course_detail', pk=self.object.pk)
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_enrolled'] = Enrollment.objects.filter(
                user=self.request.user, course=self.object
            ).exists()

            # Проверяем, завершил ли пользователь курс
            if context['is_enrolled']:
                enrollment = Enrollment.objects.get(user=self.request.user, course=self.object)
                lessons = self.object.lessons.all()
                completed_lessons = enrollment.completed_lessons.all()
                context['course_completed'] = lessons.count() > 0 and all(lesson in completed_lessons for lesson in lessons)

        # Получаем уроки курса
        lessons = self.object.lessons.all()

        # Фильтрация и поиск
        search_query = self.request.GET.get('search', '')
        if search_query:
            lessons = lessons.filter(title__icontains=search_query)

        # Пагинация: 5 уроков на страницу
        paginator = Paginator(lessons, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['search_query'] = search_query
        return context

# Страница обучения
class CourseLearnView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/course_learn.html'
    context_object_name = 'course'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not Enrollment.objects.filter(user=self.request.user, course=self.object).exists():
            messages.error(request, "Вы не записаны на этот курс.")
            return redirect('courses:course_detail', pk=self.object.pk)

        # Получаем все уроки курса, отсортированные по порядку
        lessons = self.object.lessons.all().order_by('order')

        # Получаем текущий урок (по параметру lesson_id или первый урок)
        lesson_id = self.request.GET.get('lesson_id')
        if lesson_id:
            current_lesson = get_object_or_404(Lesson, id=lesson_id, course=self.object)
        else:
            current_lesson = lessons.first() if lessons.exists() else None

        if not current_lesson:
            messages.error(request, "В этом курсе пока нет уроков.")
            return redirect('courses:course_detail', pk=self.object.pk)

        # Получаем enrollment для отслеживания прогресса
        enrollment = Enrollment.objects.get(user=self.request.user, course=self.object)

        # Обрабатываем отметку урока как пройденного
        if 'mark_completed' in self.request.GET:
            enrollment.completed_lessons.add(current_lesson)
            messages.success(request, f"Урок '{current_lesson.title}' отмечен как пройденный!")
            return redirect('courses:course_learn', pk=self.object.pk, lesson_id=current_lesson.id)

        # Определяем предыдущий и следующий уроки
        lesson_ids = list(lessons.values_list('id', flat=True))
        current_index = lesson_ids.index(current_lesson.id) if current_lesson.id in lesson_ids else 0
        previous_lesson_id = lesson_ids[current_index - 1] if current_index > 0 else None
        next_lesson_id = lesson_ids[current_index + 1] if current_index < len(lesson_ids) - 1 else None

        context = self.get_context_data(
            object=self.object,
            current_lesson=current_lesson,
            lessons=lessons,
            previous_lesson_id=previous_lesson_id,
            next_lesson_id=next_lesson_id,
            enrollment=enrollment
        )
        return self.render_to_response(context)

# Создание нового урока. Доступно только администраторам
class LessonCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Lesson
    fields = ['title', 'content', 'video', 'order']
    template_name = 'courses/lesson_form.html'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.course = get_object_or_404(Course, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={'pk': self.kwargs['pk']})

# Редактирование урока. Доступно только администраторам
class LessonUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Lesson
    fields = ['title', 'content', 'video', 'order']
    template_name = 'courses/lesson_form.html'
    pk_url_kwarg = 'lesson_pk'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={'pk': self.kwargs['course_pk']})

# Удаление урока. Доступно только администраторам
class LessonDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Lesson
    template_name = 'courses/lesson_confirm_delete.html'
    pk_url_kwarg = 'lesson_pk'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={'pk': self.kwargs['course_pk']})

# Создание нового курса. Доступно только преподавателям (is_staff)
class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    fields = ['title', 'description', 'category', 'image']
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:course_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super().form_valid(form)

# Редактирование курса. Доступно преподавателю курса или админу
class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    fields = ['title', 'description', 'category', 'image', 'is_published']
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:course_list')

    def test_func(self):
        course = self.get_object()
        return self.request.user == course.instructor or self.request.user.is_staff

# Удаление курса. Доступно преподавателю курса или админу
class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('courses:course_list')

    def test_func(self):
        course = self.get_object()
        return self.request.user == course.instructor or self.request.user.is_staff

# Запись на курс. Только для авторизованных пользователей
@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if not course.is_published:
        messages.error(request, "This course is not available for enrollment.")
        return redirect('courses:course_list')

    if Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.info(request, "You are already enrolled in this course.")
    else:
        Enrollment.objects.create(user=request.user, course=course)
        messages.success(request, f"You have successfully enrolled in {course.title}!")

    return redirect('courses:course_detail', pk=course.pk)