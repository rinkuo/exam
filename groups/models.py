from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from departments.choices import STATUS_CHOICES, GRADE_LEVEL_CHOICES, SCHEDULE_CHOICES, GPA_CHOICES
from departments.models import Department
from subjects.models import Subject
from teachers.models import Teacher
from django.shortcuts import reverse
from django.conf import settings
from departments.base_models import BaseModel


class Group(BaseModel):

    name = models.CharField(max_length=100)
    academic_year = models.CharField(max_length=30)
    max_students = models.PositiveIntegerField()
    description = models.TextField()
    status =models.CharField(max_length=2, choices=STATUS_CHOICES)
    grade_level = models.CharField(max_length=2, choices=GRADE_LEVEL_CHOICES)
    schedule = models.CharField(max_length=2, choices=SCHEDULE_CHOICES, default='in')
    subjects = models.ManyToManyField(Subject, related_name='groups', blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='groups', blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default= 1, null = False)
    gpa = models.CharField(max_length=10, choices=GPA_CHOICES, default='0')
    attendance = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    , default='0')

    def get_detail_url(self):
        return reverse('groups:detail', args=[self.pk])

    def get_update_url(self):
        return reverse('groups:update', args=[self.pk])

    def get_delete_url(self):
        return reverse('groups:delete', args=[self.pk])

    def __str__(self):
        return f"{self.name}"



