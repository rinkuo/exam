from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from .models import Department
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import DepartmentForm
from teachers.models import Teacher
from students.models import Student
from groups.models import Group
from subjects.models import Subject
from django.views.generic import ListView
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now
from datetime import datetime
class HomePageView(ListView):
    model = Student
    template_name = 'dashboard.html'
    context_object_name = 'students'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        current_students = Student.objects.count()
        first_day_of_this_month = timezone.now().replace(day=1)
        last_month_end = first_day_of_this_month - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)

        last_month_students = Student.objects.filter(
            created_at__range=[last_month_start, last_month_end]
        ).count()

        percentage_change = ((current_students - last_month_students) / last_month_students) * 100 if last_month_students > 0 else 0

        subjects = Subject.objects.all()
        subject_names = [subject.name for subject in subjects if subject and subject.name]
        subject_teacher_counts = [subject.teachers.count() for subject in subjects]

        recent_activities = []
        recent_activities += [
            {"title": "New Student Enrolled", "description": f"{student.first_name} {student.last_name} joined Group A", "time": student.created_at.strftime('%Y-%m-%d %H:%M:%S')}
            for student in Student.objects.filter(created_at__gte=timezone.now() - timedelta(days=7)).order_by('-created_at')[:5]
        ]
        recent_activities += [
            {"title": "New Teacher Added",
             "description": f"{teacher.first_name} {teacher.last_name} assigned to teach {', '.join([subject.name for subject in teacher.subjects.all()])}",
             "time": teacher.created_at.strftime('%Y-%m-%d %H:%M:%S')}
            for teacher in
            Teacher.objects.filter(created_at__gte=timezone.now() - timedelta(days=7)).order_by('-created_at')[:5]
        ]

        recent_activities += [
            {"title": "New Group Created",
             "description": f"Group {group.name} created under {group.department.name if group.department else 'No Department'}",
             "time": group.created_at.strftime('%Y-%m-%d %H:%M:%S')}
            for group in
            Group.objects.filter(created_at__gte=timezone.now() - timedelta(days=7)).order_by('-created_at')[:5]
        ]

        groups = Group.objects.all()
        teachers = Teacher.objects.all()


        current_year = datetime.now().year
        last_year = current_year - 1

        current_month = now().month
        
        enrollments_current = [
            Student.objects.filter(date_created__year=current_year, date_created__month=month).count()
            for month in range(1, current_month + 1)
        ]
        enrollments_last = [
            Student.objects.filter(date_created__year=last_year, date_created__month=month).count()
            for month in range(1, 13)
        ]



        ctx.update({
            'subject_names': subject_names,
            'subject_teacher_counts': subject_teacher_counts,
            'teachers': teachers,
            'groups': groups,
            'subjects': subjects,
            'groups_count': groups.filter(status='ac').count(),
            'current_students': current_students,
            'last_month_students': last_month_students,
            'percentage_change': percentage_change,
            'total_teachers': teachers.count(),
            'new_teachers_this_month': teachers.filter(
                created_at__range=[first_day_of_this_month, timezone.now()]
            ).count(),
            'active_groups': groups.filter(status='ac').count(),
            'new_groups_this_month': groups.filter(
                created_at__range=[first_day_of_this_month, timezone.now()]
            ).count(),
            'total_subjects': subjects.count(),
            'subjects_no_change': Subject.objects.filter(
                created_at__range=[last_month_start, last_month_end]
            ).count() == 0,
            'recent_activities': recent_activities,
            'enrollments_current' : enrollments_current,
            'enrollments_last' : enrollments_last,
            'current_year' : current_year,
            'last_year' : last_year,

        })

        return ctx

class DepartmentListView(ListView):
    model = Department
    template_name = 'departments/list.html'
    context_object_name = 'departments'
    paginate_by = 10

    def get_queryset(self):
        departments = Department.objects.all()
        head_of_department = self.request.GET.get('head_of_department')
        status = self.request.GET.get('status')
        search_query = self.request.GET.get('search')

        if head_of_department:
            departments = departments.filter(head_of_department=head_of_department)
        if status:
            departments = departments.filter(status=status)
        if search_query:
            departments = departments.filter(name__icontains=search_query)

        return departments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page')
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        departments_page = paginator.get_page(page)

        context['departments'] = departments_page
        context['paginator'] = paginator
        return context


class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/form.html'
    success_url = reverse_lazy('departments:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class DepartmentDetailView(DetailView):
    model = Department
    template_name = 'departments/detail.html'
    context_object_name = 'department'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        department = ctx['department']

        ctx['students_total'] = Student.objects.filter(group__department=department).count()
        ctx['subjects_active'] = Subject.objects.filter(department=department, status='ac').count()
        ctx['subjects'] = Subject.objects.filter(department=department)
        ctx['students'] = Student.objects.filter(group__department=department)

        return ctx

class DepartmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/form.html'
    success_url = reverse_lazy('departments:list')
    context_object_name = 'department'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        department = self.get_object()
        return self.request.user == department.author

class DepartmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Department
    template_name = 'departments/confirm_delete.html'
    success_url = reverse_lazy('departments:list')

    def test_func(self):
        department = self.get_object()
        return self.request.user == department.author
