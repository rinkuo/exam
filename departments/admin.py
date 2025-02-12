from django.contrib import admin
from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'status', 'head_of_department', 'author')
    search_fields = ('name', 'email')
    list_filter = ('status', 'head_of_department')
