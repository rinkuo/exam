from django.db import models
from .base_models import BaseModel
from django.shortcuts import reverse
from django.conf import settings
from .choices import STATUS_CHOICES


class Department(BaseModel):

    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.TextField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=13)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='in')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    head_of_department = models.CharField(max_length=100, )


    def get_detail_url(self):
        return reverse('departments:detail', args=[self.pk])

    def get_update_url(self):
        return reverse('departments:update', args=[self.pk])

    def get_delete_url(self):
        return reverse('departments:delete', args=[self.pk])

    def __str__(self):
        return f"{self.name}"