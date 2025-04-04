from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Course, Enrollment
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from .forms import CourseForm

def home(request):
    return render(request, 'base.html')
class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Course.objects.all()
        return Course.objects.filter(is_published=True)


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_enrolled'] = Enrollment.objects.filter(
                user=self.request.user, course=self.object
            ).exists()
        return context


class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    fields = ['title', 'description', 'category', 'image']
    template_name = 'courses/course_form.html'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super().form_valid(form)


class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    fields = ['title', 'description', 'category', 'image', 'is_published']
    template_name = 'courses/course_form.html'

    def test_func(self):
        course = self.get_object()
        return self.request.user == course.instructor or self.request.user.is_staff


class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('courses:course_list')

    def test_func(self):
        course = self.get_object()
        return self.request.user == course.instructor or self.request.user.is_staff


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/../templates/users/signup.html'
    success_url = reverse_lazy('login')


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

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:course_list')

class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:course_list')

class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('courses:course_list')