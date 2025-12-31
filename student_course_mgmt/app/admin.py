from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'grade', 'age')
    search_fields = ('name', 'email')
    list_filter = ('grade',)
    ordering = ('id',)
