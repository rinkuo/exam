from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CASCADE
from django.conf import settings
from departments.base_models import BaseModel
from departments.choices import SELECT_GENDER, GRADE_LEVEL_CHOICES, STATUS_CHOICES, GPA_CHOICES
from groups.models import Group
from django.utils import timezone
from django.shortcuts import reverse
from subjects.models import Subject


class Student(BaseModel):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=13)
    address = models.TextField()
    parent_name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    parent_phone_number = models.CharField(max_length=13)
    parent_email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='students/')
    grade = models.CharField(max_length=2, choices=GRADE_LEVEL_CHOICES)
    gender = models.CharField(max_length=3, choices=SELECT_GENDER)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='in')
    group = models.ForeignKey(Group, on_delete=CASCADE, related_name='students', blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, related_name='students', blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    gpa = models.CharField(max_length=10, choices=GPA_CHOICES, default='0')
    attendance = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    , default='0')

    def get_detail_url(self):
        return reverse('students:detail', args=[self.pk])

    def get_update_url(self):
        return reverse('students:update', args=[self.pk])

    def get_delete_url(self):
        return reverse('students:delete', args=[self.pk])

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def some_function(self):
        from subjects.models import Subject