from django.utils import timezone
from django.db import models
from departments.base_models import BaseModel
from departments.choices import GRADE_LEVEL_CHOICES, STATUS_CHOICES
from departments.models import Department
from django.shortcuts import reverse
from django.conf import settings


class Subject(BaseModel):

    name = models.CharField(max_length=200)
    description = models.TextField()
    credit_hours = models.PositiveIntegerField()
    prerequisites = models.CharField(max_length=255, blank=True)
    grade_level = models.CharField(max_length=2, choices=GRADE_LEVEL_CHOICES)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='in')
    department = models.ForeignKey(Department,  on_delete=models.CASCADE, related_name='subjects', null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def prerequisite_list(self):
        return [prerequisite.strip() for prerequisite in self.prerequisites.split(',')] if self.prerequisites else []

    def get_detail_url(self):
        return reverse('subjects:detail', args=[self.pk])

    def get_update_url(self):
        return reverse('subjects:update', args=[self.pk])

    def get_delete_url(self):
        return reverse('subjects:delete', args=[self.pk])

    def __str__(self):
        return f"{self.name}"
